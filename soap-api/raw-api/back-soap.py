from http.server import BaseHTTPRequestHandler, HTTPServer
import xml.etree.ElementTree as ET
import pandas as pd
import secrets


# TODO: Put token and user database in a database
TOKENS = {}
USERS_DATABASE = pd.read_csv('/home/zakaria/Documents/scolaire/ensiie/2A/architecture-systemes-info/sysinfo_auto_ws_project/database/train_booking_ws/user_table.csv')

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
        # Check for authentication token in the SOAP header
        elif root.find('.//Token') is None or not self.is_authenticated(root.find('.//Token').text):
            return "Unauthorized"
        elif method_name == 'HelloWorld':
            return "Hello, " + parameters.get('Name')
        elif method_name == 'GetUserInfo':
            return f"User ID: {parameters.get('UserID')}, User Type: {parameters.get('UserType')}"
        elif method_name == 'TrainSearch':
            # TODO: Appeler l'API Rest
            # TODO: Parser la réponse: liste d'ID de trains, liste de prix, listes types de ticket (flexible, non flexible)
            # TODO: Ou sinon return "No available trains"
            return "Train search results"
        elif method_name == 'TrainBooking':
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

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SOAPServer)
    print("SOAP server running on port 8000")
    httpd.serve_forever()
