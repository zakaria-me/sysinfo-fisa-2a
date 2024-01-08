# Student names

- Maxime CARDINALE
- Zakaria MELLAH

# How to run the services

In a linux environment, place yourself at the root of the this folder (where this README lies).
The project contains three services:
- A REST API implemented with django
- A SOAP API implemented with spyne
- A Web Client written in flask

Note: the project uses the ports 8009, 8000 and 5000
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

In 3 seperate terminals:

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