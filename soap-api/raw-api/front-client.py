from flask import Flask, request, render_template_string, redirect, url_for, render_template
import requests
import json

from zeep import Client, exceptions


WSDL_URL = 'http://localhost:8009/?wsdl'
client = Client(WSDL_URL)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():


    username = request.form['username']
    password = request.form['password']

    try:
        soap_response = client.service.login(username, password)
    except exceptions.Fault as fault:
        return render_template('index.html', message=fault.message) 

    return render_template('train_search.html', soap_response=soap_response) 

@app.route('/create_user', methods=['POST'])
def create_user():
    username = request.form['username']
    password = request.form['password']

    response = client.service.create_user(username, password)

    return render_template('index.html', message=response)

@app.route('/train_search', methods=['POST'])
def train_search_ws():
    token = request.form['token']
    GareDepart = request.form['GareDepart']
    GareArrivee = request.form['GareArrivee']
    DateDepart = request.form['DateDepart']
    DateArrivee = request.form['DateArrivee']
    NombreTicket = request.form['NombreTickets']
    Classe = request.form['Classe']

    try:
        response = client.service.train_search(token, GareDepart, GareArrivee, DateDepart, DateArrivee, NombreTicket, Classe)
    except exceptions.Fault as fault:
        return fault.message
    response = json.loads(response)
    trains = response['results'] 
    trains_ids = [train['id'] for train in trains]
    number_of_trains = response['count'] 

    return render_template('train_search.html', soap_response=token, trains=trains, number_of_trains=number_of_trains, 
                           trains_ids=trains_ids) 

@app.route('/train_booking', methods=['POST'])
def train_booking_ws():
    token = request.form['token']
    typeTravel = request.form['typeTravel']
    trainAway = request.form['trainAway']
    trainRound = request.form['trainRound']
    Classe = request.form['Classe']
    TypeTicket = request.form['TypeTicket']
    NombreTicket = request.form['NombreTickets']

    try:
        r = client.service.train_booking(token, typeTravel, trainAway, trainRound, Classe, TypeTicket, NombreTicket)
    except exceptions.Fault as fault:
        return fault.message

    return render_template('train_search.html', soap_response=token, booked=r)

def get_token(username, password):
    url = "http://localhost:8004/"
    headers = {'content-type': 'text/xml'}

    # Sample SOAP request body for login
    body = f'''<?xml version="1.0"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                        xmlns:ns="train_webservice">
        <SOAP-ENV:Body>
            <ns:Login>
                <Username>{username}</Username>
                <Password>{password}</Password>
            </ns:Login>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

    response = requests.post(url, data=body, headers=headers)
    return response.content  # This should be parsed to extract the token

def test_hello_world_authenticated(token):
    url = "http://localhost:8004/"
    headers = {'content-type': 'text/xml'}


    # Sample SOAP request body
    body = f'''<?xml version="1.0"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                        xmlns:ns="train_webservice">
        <SOAP-ENV:Body>
            <SOAP-ENV:Header>
                <Token>{token}</Token>
            </SOAP-ENV:Header>
            <ns:HelloWorld>
                <Name>John Doe</Name>
            </ns:HelloWorld>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

    response = requests.post(url, data=body, headers=headers)
    return response.content

def train_search(token, GareDepart, GareArrivee, DateDepart, DateArrivee, NombreTicket, Classe):
    url = "http://localhost:8004/"
    headers = {'content-type': 'text/xml'}


    # Sample SOAP request body
    body = f'''<?xml version="1.0"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                        xmlns:m="http://www.example.org/stock">
        <SOAP-ENV:Body>
            <SOAP-ENV:Header>
                <Token>{token}</Token>
            </SOAP-ENV:Header>
            <m:TrainSearch>
                <GareDepart>{GareDepart}</GareDepart>
                <GareArrivee>{GareArrivee}</GareArrivee>
                <DateDepart>{DateDepart}</DateDepart>
                <DateArrivee>{DateArrivee}</DateArrivee>
                <NombreTicket>{NombreTicket}</NombreTicket>
                <Classe>{Classe}</Classe>
            </m:TrainSearch>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

    response = requests.post(url, data=body, headers=headers)
    return response.content

def train_booking(token, trainId, Classe, TypeTicket, NombreTicket):
    url = "http://localhost:8004/"
    headers = {'content-type': 'text/xml'}


    # Sample SOAP request body
    body = f'''<?xml version="1.0"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                        xmlns:m="http://www.example.org/stock">
        <SOAP-ENV:Body>
            <SOAP-ENV:Header>
                <Token>{token}</Token>
            </SOAP-ENV:Header>
            <m:TrainBooking>
                <trainId>{trainId}</trainId>
                <Classe>{Classe}</Classe>
                <TypeTicket>{TypeTicket}</TypeTicket>
                <NombreTicket>{NombreTicket}</NombreTicket>
            </m:TrainBooking>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

    response = requests.post(url, data=body, headers=headers)
    return response.content

if __name__ == '__main__':
    app.run(debug=True)
