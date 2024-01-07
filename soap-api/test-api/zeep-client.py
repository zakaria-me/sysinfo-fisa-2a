from zeep import Client
import requests
import logging


# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('zeep.transports')
# logger.setLevel(logging.DEBUG)


# URL to the WSDL of the SOAP service
wsdl_url = 'http://localhost:8009/?wsdl'

# Create a client using the WSDL
client = Client(wsdl_url)

# Call the 'say_hello' service
response = client.service.say_hello('John', 3)

print(response)


url = 'http://localhost:8009/'

soap_request = """<?xml version='1.0' encoding='utf-8'?>
<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
<soap-env:Body>
<ns0:say_hello xmlns:ns0="spyne.examples.hello">
<ns0:name>John</ns0:name>
<ns0:times>3</ns0:times>
</ns0:say_hello>
</soap-env:Body>
</soap-env:Envelope>
"""
headers = {
    "Content-Type": "text/xml;charset=UTF-8",
    "SOAPAction": ""  # SOAPAction may be required depending on the service
}

response = requests.post(url, data=soap_request, headers=headers)

print(response.content)
