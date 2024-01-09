#!/bin/bash

source wsproject/bin/activate

python rest_api/manage.py runserver &

sleep 2

python soap-api/raw-api/back-soap.py &

sleep 2

python soap-api/raw-api/front-client.py &