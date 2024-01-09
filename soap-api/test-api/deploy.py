from wsgiref.simple_server import make_server

if __name__ == '__main__':
    server = make_server('127.0.0.1', 8000, WsgiApplication(application))
    print("SOAP service is running on http://127.0.0.1:8000")
    print("WSDL is at: http://127.0.0.1:8000/?wsdl")
    server.serve_forever()
