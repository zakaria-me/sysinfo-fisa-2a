# Student names

- Maxime CARDINALE
- Zakaria MELLAH

# How to run the services

In a linux environment, place yourself at the root of the this folder (where this README lies).
The project contains three services:
- A REST API implemented with django
- A SOAP API implemented with spyne
- A Web Client written in flask

Note: the project uses the ports 8009 (SOAP API), 8000(REST API) and 5000(Web Client)

Make sure they are available.

Initialize a virtual environement:
```bash
python -m venv wsproject/
source wsproject/bin/activate
```

Install the necessary librairies:
```bash
pip install -r requirements.txt
```

## In one terminal (limited output)

```bash
bash launch.sh
```

## In 3 seperate terminals:

Terminal 1:
```bash
python rest_api/manage.py migrate
python rest_api/manage.py runserver 
```

Terminal 2:
```bash
python soap-api/raw-api/back-soap.py
```

Terminal 3:
```bash
python soap-api/raw-api/front-client.py
```

### Description of the services

- The SOAP API is available at 127.0.0.1:8009 and its WSDL at 127.0.0.1:8009/?wsdl
- The REST API is available at 127.0.0.1:8000
- The web client is available at 127.0.0.1:5000
- You can alos find the WSDL of the SOAP service in this repo at soap-api/wsdl.xml

# Self-evaluation
## 	Requirements 	                                                                Marks (30)
1 	Create REST Train Filtering service B 	                                            6/6

2 	Create SOAP Train Booking service A 	                                            4/4

3 	Interaction between two services 	                                                4/4

4 	Test with Web service Client (instead of using Eclipse's Web service Explorer)  	2/2

5 	Work with complex data type (class, table, etc.) 	                                2/2

6 	Work with database (in text file, xml, in mysql, etc.) 	                            2/2

7 	Postman 	                                                                        1.5/2

8 	OpenAPI 	                                                                        2/3

9 	BPMS 	                                                                            0/5

# Documentation de l'API

Le lien vers la documentation de l'API (réalisée avec Swagger) est disponible à ce lien https://app.swaggerhub.com/apis-docs/MDCCARDINALE/REST/2.0.2
Si le lien n'est plus fonctionnel, vous pouvez retrouver le fichier swagger source dans le dossier rest_api/swagger.yaml

# Test de l'API REST avec POSTMAN

Vous pouvez trouver la collection POSTMAN associée dans le dossier postman/

# Test de l'API SOAP avec POSTMAN


## Create user 

L'API demande une authentification pour chaque appel. Nous avons besoin d'un utilisateur qui puisse ensuite demander un token.

Dans Postman, dans l'onglet 'Headers', on ajoute un paramètre 'Content-type = text/xml".  Dans l'onglet 'Body', on coche 'raw' et le format 'XML'. Puis, on remplit le body:

### Appel

```xml
<?xml version='1.0' encoding='utf-8'?>
<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
<soap-env:Body>
    <ns0:create_user xmlns:ns0="train_webservice">
        <ns0:username>username</ns0:username>
        <ns0:password>password</ns0:password>
        </ns0:create_user></soap-env:Body>
        </soap-env:Envelope>
```

### Reponse si aucune erreur

```xml
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="train_webservice">
    <soap11env:Body>
        <tns:create_userResponse>
            <tns:create_userResult>User created</tns:create_userResult>
        </tns:create_userResponse>
    </soap11env:Body>
</soap11env:Envelope>
```

## Login

L'API demande un token pour chaque appel à l'API. Il faut se connecter pour en récupérer un.

Dans Postman, dans l'onglet 'Headers', on ajoute un paramètre 'Content-type = text/xml".  Dans l'onglet 'Body', on coche 'raw' et le format 'XML'. Puis, on remplit le body:

### Appel

```xml
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
```

### Reponse si aucune erreur

```xml
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="train_webservice">
    <soap11env:Body>
        <tns:loginResponse>
            <tns:loginResult>token</tns:loginResult>
        </tns:loginResponse>
    </soap11env:Body>
</soap11env:Envelope>
```

## Train Search 

Pour faire une recherche de Train disponible

Dans Postman, dans l'onglet 'Headers', on ajoute un paramètre 'Content-type = text/xml".  Dans l'onglet 'Body', on coche 'raw' et le format 'XML'. Puis, on remplit le body:

### Appel

```xml
<?xml version='1.0' encoding='utf-8'?>
<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
<soap-env:Body>
    <ns0:train_search xmlns:ns0="train_webservice">
        <ns0:token>token</ns0:token>
        <ns0:GareDepart></ns0:GareDepart>
        <ns0:GareArrivee></ns0:GareArrivee>
        <ns0:DateDepart></ns0:DateDepart>
        <ns0:DateArrivee></ns0:DateArrivee>
        <ns0:NombreTicket></ns0:NombreTicket>
        <ns0:Classe> </ns0:Classe>
    </ns0:train_search>
    </soap-env:Body>
</soap-env:Envelope>
```

### Reponse si aucune erreur

```xml
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="train_webservice">
    <soap11env:Body>
        <tns:train_searchResponse>
            <tns:train_searchResult>data_en_format_json</tns:train_searchResult>
        </tns:train_searchResponse>
    </soap11env:Body>
</soap11env:Envelope>
```

## Train Booking 

Pour faire une recherche de Train disponible

Dans Postman, dans l'onglet 'Headers', on ajoute un paramètre 'Content-type = text/xml".  Dans l'onglet 'Body', on coche 'raw' et le format 'XML'. Puis, on remplit le body:

### Appel

```xml
<?xml version='1.0' encoding='utf-8'?>
<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
<soap-env:Body><ns0:train_booking xmlns:ns0="train_webservice">
    <ns0:token>token</ns0:token>
    <ns0:typeTravel>oneWay/roundTrip</ns0:typeTravel>
    <ns0:trainAway>5269</ns0:trainAway>
    <ns0:Classe>Standard</ns0:Classe>
    <ns0:TypeTicket>flexible</ns0:TypeTicket>
    <ns0:NombreTicket>4</ns0:NombreTicket>
    </ns0:train_booking>
    </soap-env:Body>
</soap-env:Envelope>
```

### Reponse si aucune erreur

```xml
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="train_webservice">
    <soap11env:Body>
        <tns:train_bookingResponse>
            <tns:train_bookingResult>Successful reservation</tns:train_bookingResult>
        </tns:train_bookingResponse>
    </soap11env:Body>
</soap11env:Envelope>
```
