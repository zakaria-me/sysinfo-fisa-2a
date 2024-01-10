from zeep import Client
import requests
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('zeep.transports')
logger.setLevel(logging.DEBUG)


# URL to the WSDL of the SOAP service
wsdl_url = 'http://localhost:8009/?wsdl'

# Create a client using the WSDL
client = Client(wsdl_url)

response = client.service.login('Mellah', 1234)
print(response)
# r = client.service.train_booking(response, 'oneWay', '5269', None, 'Standard', 'flexible', '4')
# print(response)


url = 'http://localhost:8009/'

soap_request = """
<?xml version='1.0' encoding='utf-8'?>
<soap-env:Envelope 
xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
<soap-env:Body>
<ns0:login xmlns:ns0="train_webservice">
<ns0:username>Mellah</ns0:username>
<ns0:password>1234</ns0:password>
</ns0:login>
</soap-env:Body>
</soap-env:Envelope>
"""
headers = {
    "Content-Type": "text/xml;charset=UTF-8",
    "SOAPAction": ""  # SOAPAction may be required depending on the service
}

# response = requests.post(url, data=soap_request, headers=headers)

# print(response.content)
