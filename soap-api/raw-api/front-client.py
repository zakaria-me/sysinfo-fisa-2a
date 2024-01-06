from flask import Flask, request, render_template_string, redirect, url_for, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Prepare and send the SOAP request
    soap_response = get_token(username, password)
    soap_response = soap_response.decode('utf-8').split('<Response>')[1].split('</Response>')[0]
    

    return render_template('train_search.html', soap_response=soap_response) 

@app.route('/train_search', methods=['POST'])
def train_search_ws():
    token = request.form['token']
    GareDepart = request.form['GareDepart']
    GareArrivee = request.form['GareArrivee']
    DateDepart = request.form['DateDepart']
    DateArrivee = request.form['DateArrivee']
    HeureDepart = request.form['HeureDepart']
    HeureArrivee = request.form['HeureArrivee']
    NombreTicket = request.form['NombreTicket']
    Classe = request.form['Classe']

    response = train_search(token, GareDepart, GareArrivee, DateDepart, DateArrivee, HeureDepart, HeureArrivee, NombreTicket, Classe) 
    response = response.decode('utf-8').split('<Response>')[2].split('</Response>')[0]

    return render_template('train_search.html', soap_response=token, trains=response) 

@app.route('/train_booking', methods=['POST'])
def train_booking_ws():
    token = request.form['token']
    trainId = request.form['trainId']
    Classe = request.form['Classe']
    TypeTicket = request.form['TypeTicket']

    response = train_booking(token, trainId, Classe, TypeTicket) 
    response = response.decode('utf-8').split('<Response>')[2].split('</Response>')[0]

    return render_template('train_search.html', soap_response=token, error=response) 


def get_token(username, password):
    url = "http://localhost:8000/"
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
    url = "http://localhost:8000/"
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

def train_search(token, GareDepart, GareArrivee, DateDepart, DateArrivee, HeureDepart, HeureArrivee, NombreTicket, Classe):
    url = "http://localhost:8000/"
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
                <HeureDepart>{HeureDepart}</HeureDepart>
                <HeureArrivee>{HeureArrivee}</HeureArrivee>
                <NombreTicket>{NombreTicket}</NombreTicket>
                <Classe>{Classe}</Classe>
            </m:TrainSearch>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

    response = requests.post(url, data=body, headers=headers)
    return response.content

def train_booking(token, trainId, Classe, TypeTicket):
    url = "http://localhost:8000/"
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
            </m:TrainBooking>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

    response = requests.post(url, data=body, headers=headers)
    return response.content

if __name__ == '__main__':
    app.run(debug=True)
