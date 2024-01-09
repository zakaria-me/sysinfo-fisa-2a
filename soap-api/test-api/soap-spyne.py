from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class HelloWorldService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Unicode)
    def say_hello(ctx, name, times):
        return 'Hello, %s' % name * times

class LoginService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Unicode)
    def say_hello(ctx, name, times):
        return 'Hello, %s' % name * times
    
class CreateUser(ServiceBase):
    @rpc(Unicode, Integer, _returns=Unicode)
    def say_hello(ctx, name, times):
        return 'Hello, %s' % name * times

class TrainSearchService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Unicode)
    def say_hello(ctx, name, times):
        return 'Hello, %s' % name * times


class TrainBookingService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Unicode)
    def say_hello(ctx, name, times):
        return 'Hello, %s' % name * times
    

# Create the application
application = Application([HelloWorldService],
                          tns='spyne.examples.hello',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

from wsgiref.simple_server import make_server

if __name__ == '__main__':
    server = make_server('127.0.0.1', 8009, WsgiApplication(application))
    print("SOAP service is running on http://127.0.0.1:8009")
    print("WSDL is at: http://127.0.0.1:8009/?wsdl")
    server.serve_forever()
