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

# Self-evaluation
## 	Requirements 	                                                                Marks (30)
1 	Create REST Train Filtering service B 	                                            6/6

2 	Create SOAP Train Booking service A 	                                            4/4

3 	Interaction between two services 	                                                4/4

4 	Test with Web service Client (instead of using Eclipse's Web service Explorer)  	2/2

5 	Work with complex data type (class, table, etc.) 	                                1/2

6 	Work with database (in text file, xml, in mysql, etc.) 	                            2/2

7 	Postman 	                                                                        2/2

8 	OpenAPI 	                                                                        3/3

9 	BPMS 	                                                                            0/5

