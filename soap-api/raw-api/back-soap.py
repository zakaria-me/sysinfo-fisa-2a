from http.server import BaseHTTPRequestHandler, HTTPServer
import xml.etree.ElementTree as ET
import pandas as pd
import secrets
import requests


# TODO: Put token and user database in a database
TOKENS = {}
# TODO: delete absolute path
# USERS_DATABASE = pd.read_csv('/home/zakaria/Documents/scolaire/ensiie/2A/architecture-systemes-info/sysinfo_auto_ws_project/database/train_booking_ws/user_table.csv')
# USERS_DATABASE_PATH = r'C:\Users\9609024S\Documents\tuto-bac-a-sable\sysinfo_auto_ws_project\database\train_booking_ws\user_table.csv' 
USERS_DATABASE_PATH = "database/train_booking_ws/user_table.csv" 

from spyne import Application, rpc, ServiceBase, Integer, Unicode, Fault
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class LoginService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Unicode)
    def login(ctx, username, password):
        print(username, password)
        if is_valid_user(username, password):
            token = secrets.token_hex(16)
            TOKENS[token] = username 
            return token 
        else:
            raise Fault(faultcode="Unauthorized", faultstring="Invalid username or password") 

class CreateUserService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Unicode)
    def create_user(ctx, username, password):
        if is_valid_user(username, password):
            return "User already exists"
        else:
            # add user to the USERS_DATABASE pandas dataframe
            users_database = pd.read_csv(USERS_DATABASE_PATH)
            users_database =  pd.concat([users_database, pd.DataFrame({'NomUtilisateur': [username], 'MotDePasse': [password]})])
            users_database.to_csv(USERS_DATABASE_PATH, index=False)
            return "User created"

class TrainSearchService(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def train_search(ctx,token, GareDepart, GareArrivee, DateDepart, DateArrivee, NombreTicket, Classe):
        if not is_authenticated(token):
            raise Fault(faultcode="Unauthorized", faultstring="Invalid token")

        data = {}

        if GareDepart is not None:
            data['departure_station'] = GareDepart
        if GareArrivee is not None:
            data['arrival_station'] = GareArrivee
        if DateDepart is not None:
            data['departure_date'] = DateDepart
        if DateArrivee is not None:
            data['arrival_date'] = DateArrivee
        if Classe is not None:
            if Classe == 'Standard':
                if NombreTicket is None:
                    return "Missing number of tickets"
                data['standard_class_seats'] = NombreTicket
            elif Classe == 'First':
                if NombreTicket is None:
                    return "Missing number of tickets"
                data['first_class_seats'] = NombreTicket
            elif Classe == 'Business':
                if NombreTicket is None:
                    return "Missing number of tickets"
                data['business_class_seats'] = NombreTicket
        
        print("Parameters: ", data)
        r = requests.get('http://127.0.0.1:8000/trains/', params=data)

        if r.status_code != 200:
            if r.status_code == 204:
                raise Fault(faultcode="InternalServerError", faultstring="No available trains")
            raise Fault(faultcode="InternalServerError", faultstring=r.text)
        else:
            return r.content

class TrainBookingService(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def train_booking(ctx, token, typeTravel, trainAway, trainRound, Classe, TypeTicket, NombreTicket):
        if not is_authenticated(token):
            raise Fault(faultcode="Unauthorized", faultstring="Invalid token")
        
        print(typeTravel, trainAway, trainRound, Classe, TypeTicket, NombreTicket)
        if typeTravel == 'oneWay' and trainAway is None:
            return "Missing trainAway Id"
        if typeTravel == 'roundTrip' and (trainAway is None or trainRound is None):
            return "Missing trainAway or trainRound Id"
        if typeTravel == 'roundTrip' and (trainAway == trainRound):
            return "Same train Ids"

        data = {}
        if Classe is not None:
            if Classe == 'Standard':
                data['seat_type'] = 'standard' 
            elif Classe == 'First':
                data['seat_type'] = 'first' 
            elif Classe == 'Business':
                data['seat_type'] = 'business' 

        if TypeTicket is not None:
            if TypeTicket == 'flexible':
                data['ticket_type'] = 'flexible'

        if NombreTicket is not None:
            data['quantity'] = int(NombreTicket) 

        if typeTravel == 'oneWay':
            r = requests.post(f'http://127.0.0.1:8000/trains/{trainAway}/seats_reservation/',data=data)
            print("data " + str(data))
            if r.status_code != 200:
                raise Fault(faultcode="InternalServerError", faultstring=r.text)
            return "Successful reservation"
        if typeTravel == 'roundTrip':
            r = requests.post(f'http://127.0.0.1:8000/trains/{trainAway}/seats_reservation/',data=data)
            if r.status_code != 200:
                raise Fault(faultcode="InternalServerError", faultstring=f"Reservation error on the train {trainAway} is not avaialble")
            r = requests.post(f'http://127.0.0.1:8000/trains/{trainRound}/seats_reservation/',data=data)
            if r.status_code != 200:
                raise Fault(faultcode="InternalServerError", faultstring=f"Reservation error on the train {trainRound} is not avaialble")
            return "Successful reservation"
            
def is_valid_user(username, password):
    users_database = pd.read_csv(USERS_DATABASE_PATH)
    for i, (index,row) in enumerate(users_database.iterrows()):
        if str(row['NomUtilisateur']) == str(username) and str(row['MotDePasse']) == str(password):
            return True
    return False

def is_authenticated(token):
    if token in TOKENS:
        return True 
    return False

# Create the application
application = Application([LoginService, CreateUserService, TrainSearchService, TrainBookingService],
                          tns='train_webservice',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

from wsgiref.simple_server import make_server

if __name__ == '__main__':
    server = make_server('127.0.0.1', 8009, WsgiApplication(application))
    print("SOAP service is running on http://127.0.0.1:8009")
    print("WSDL is at: http://127.0.0.1:8009/?wsdl")
    server.serve_forever()
