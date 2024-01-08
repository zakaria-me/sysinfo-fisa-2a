from http.server import BaseHTTPRequestHandler, HTTPServer
import xml.etree.ElementTree as ET
import pandas as pd
import secrets
import requests


# TODO: Put token and user database in a database
# TODO: Add a method to create a user
TOKENS = {}
# TODO: delete absolute path
# USERS_DATABASE = pd.read_csv('/home/zakaria/Documents/scolaire/ensiie/2A/architecture-systemes-info/sysinfo_auto_ws_project/database/train_booking_ws/user_table.csv')
USERS_DATABASE_PATH = r'C:\Users\9609024S\Documents\tuto-bac-a-sable\sysinfo_auto_ws_project\database\train_booking_ws\user_table.csv' 

class SOAPServer(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Parse the XML data
        tree = ET.ElementTree(ET.fromstring(post_data))
        root = tree.getroot()

        # Extract the SOAP body and find the method being called
        soap_body = root.find('{http://schemas.xmlsoap.org/soap/envelope/}Body')
        if soap_body is not None:
            for method_call in soap_body:
                method_name = method_call.tag
                # Strip namespace if present
                method_name = method_name[method_name.find('}')+1:]
                parameters = {child.tag: child.text for child in method_call}
                response_value = self.handle_method(method_name, parameters, root)

                if response_value == "Unauthorized":
                    # TODO: Send SOAP error: the body contains a FAULT element
                    self.send_error(401, "Unauthorized")
                    return

                # Create and send the SOAP response
                self.send_soap_response(response_value)

    def is_authenticated(self, token):
    # In a real scenario, this method would check the token's validity, e.g., against a database
    # For demonstration, we'll use a hardcoded token
        if token in TOKENS:
            return True 
        return False

    def is_valid_user(self, username, password):
        # In a real scenario, this method would check the username and password against a database
        # For demonstration, we'll use hardcoded values
        password_database = USERS_DATABASE[USERS_DATABASE['NomUtilisateur'] == username]['MotDePasse'][0]
        return str(password_database) == str(password)

    def send_token(self, token):
        # Create a response with the token
        soap_response = f'''<?xml version="1.0"?>
        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP-ENV:Body>
                <Token>{token}</Token>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>'''

        # Send response
        self.send_response(200)
        self.send_header('Content-Type', 'text/xml')
        self.end_headers()
        self.wfile.write(soap_response.encode())


    def handle_method(self, method_name, parameters, root):

        if method_name == 'Login':
            if 'Username' not in parameters or 'Password' not in parameters:
                return "Missing username or password"
            username = parameters.get('Username')
            password = parameters.get('Password')
            if self.is_valid_user(username, password):
                token = secrets.token_hex(16)
                TOKENS[token] = username 
                return token 
            else:
                return "Invalid username or password"
        elif method_name == 'CreateUser':
            if 'Username' not in parameters or 'Password' not in parameters:
                return "Missing username or password"
            username = parameters.get('Username')
            password = parameters.get('Password')
            if self.is_valid_user(username, password):
                return "User already exists"
            else:
                USERS_DATABASE.append({'NomUtilisateur': username, 'MotDePasse': password})
                return "User created"
        # Check for authentication token in the SOAP header
        elif root.find('.//Token') is None or not self.is_authenticated(root.find('.//Token').text):
            return "Unauthorized"
        elif method_name == 'HelloWorld':
            return "Hello, " + parameters.get('Name')
        elif method_name == 'GetUserInfo':
            return f"User ID: {parameters.get('UserID')}, User Type: {parameters.get('UserType')}"
        elif method_name == 'TrainSearch':
            # Iterate through all the parameters and add them to a data dictionary if they are not None
            parameters_translator = {
                'GareDepart': 'departure_station',
                'GareArrivee': 'arrival_station',
                'DateDepart': 'departure_date',
                'DateArrivee': 'arrival_date',
            }
            data = {}
            for key, value in parameters.items():
                if value is not None:
                    if key == 'Classe':
                        if value == 'Standard':
                            key = 'standard_class_seats'
                        elif value == 'First':
                            key = 'first_class_seats'
                        elif value == 'Business':
                            key = 'business_class_seats'
                        elif value == 'NoPreference':
                            # data['seats_number'] = parameters.get('NombreTickets')
                            continue
                        # Si une classe est spécifiée,, il y a forcément un nombre de tickets associé
                        if parameters.get('NombreTickets') is None:
                            return "Missing number of tickets"
                        data[key] = parameters.get('NombreTickets')
                    else:
                        data[parameters_translator[key]] = value

            # Make a request to the API
            r = requests.get('http://127.0.0.1:8000/trains/', params=data)

            if r.status_code != 200:
                return "No available trains"
            else:
                return r.content
        elif method_name == 'TrainBooking':
            parameters_translator = {
                'trainId': 'train_id',
                'TypeTicket': 'ticket_type',
                'NombreTicket': 'quantity',
            }

            data = {}
            for key, value in parameters.items():
                if value is not None:
                    if key == 'Classe':
                        if value == 'Standard':
                            data[parameters_translator[key]] = 'standard'
                        elif value == 'First':
                            data[parameters_translator[key]] = 'first'
                        elif value == 'Business':
                            data[parameters_translator[key]] = 'business'
                    else:
                        data[parameters_translator[key]] = value


            

            # TODO: Choisir un train ou deux pour un voyage aller-retour
            # TODO: parser la réponse: True ou False
            return "Successful reservation"
            return "Reservation error on the train + ID + is not avaialble" 
        else:
            return "Unknown method"

    def send_soap_response(self, response_value):
        soap_response = f'''<?xml version="1.0"?>
        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP-ENV:Body>
                <Response>{response_value}</Response>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>'''

        self.send_response(200)
        self.send_header('Content-Type', 'text/xml')
        self.end_headers()
        self.wfile.write(soap_response.encode())

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
            return "Invalid username or password"

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
            return "Unauthorized"

        parameters_translator = {
            'GareDepart': 'departure_station',
            'GareArrivee': 'arrival_station',
            'DateDepart': 'departure_date',
            'DateArrivee': 'arrival_date',
        }
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
            print(r.status_code)
            if r.status_code == 204:
                raise Fault(faultcode="InternalServerError", faultstring="No available trains")
            return "No available trains"
        else:
            return r.content

class TrainBookingService(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def train_booking(ctx, token, typeTravel, trainAway, trainRound, Classe, TypeTicket, NombreTicket):
        if not is_authenticated(token):
            return "Unauthorized"
        
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
            data['quantity'] = 3 

        if typeTravel == 'oneWay':
            r = requests.post(f'http://127.0.0.1:8000/trains/{trainAway}/seats_reservation/',data=data)
            print("data " + str(data))
            # print("Response : ", r.status_code)
            if r.status_code != 200:
                raise Fault(faultcode="InternalServerError", faultstring=r.text)
            return r.text
            if not r.content :
                return f"Reservation error on the train {trainAway} is not avaialble"
            return "Successful reservation"
        if typeTravel == 'roundTrip':
            r = requests.post(f'http://127.0.0.1:8000/trains/{trainAway}/seats_reservation/',data=data)
            if not r.content :
                return f"Reservation error on the train {trainAway} is not avaialble"
            r = requests.post(f'http://127.0.0.1:8000/trains/{trainRound}/seats_reservation/',data=data)
            if not r.content :
                return f"Reservation error on the train {trainRound} is not avaialble"
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
    # server_address = ('', 8004)
    # httpd = HTTPServer(server_address, SOAPServer)
    # print("SOAP server running on port 8004")
    # httpd.serve_forever()
