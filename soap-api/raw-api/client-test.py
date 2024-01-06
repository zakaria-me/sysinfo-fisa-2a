import requests

def test_token():
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

    # Use the function to get a token
    token = get_token('Mellah', '1234')
    # parse the token from the response
    token = token.decode('utf-8').split('<Response>')[1].split('</Response>')[0]
    print(token)
    return token

    # Then use the token in subsequent requests

def test_hello_world():
    url = "http://localhost:8000/"
    headers = {'content-type': 'text/xml'}


    # Sample SOAP request body
    body = f'''<?xml version="1.0"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
        <SOAP-ENV:Body>
            <m:GetName xmlns:m="http://www.example.org/stock">
                <Name>John Doe</Name>
            </m:GetName>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

    response = requests.post(url, data=body, headers=headers)
    print(response.content)

def test_hello_world_authenticated(token):
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
            <m:HelloWorld >
                <Name>John Doe</Name>
            </m:HelloWorld>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

    response = requests.post(url, data=body, headers=headers)
    print(response.content)

def test_raw_xml():

    body=f'''<?xml version="1.0"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                   xmlns:ns="http://www.example.com/soap">
    <SOAP-ENV:Header>
        <Token>your_auth_token</Token>
    </SOAP-ENV:Header>
    <SOAP-ENV:Body>
        <ns:GetUserInfo>
            <UserID>12345</UserID>
            <UserType>Admin</UserType>
        </ns:GetUserInfo>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>'''
    
    url = "http://localhost:8000/"
    headers = {'content-type': 'text/xml'}
    response = requests.post(url, data=body, headers=headers)
    print(response.content)

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
    print(response.content)

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
    print(response.content)


if __name__ == "__main__":
    token = test_token()
    # test_hello_world()
    # test_hello_world_authenticated(token)
    train_search(token, 'Melun', 'Paris', '21/08/2023', '21/08/2023', '05:00', '06:00', '1', 'Standard')
    # test_raw_xml()