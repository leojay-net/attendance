#!/bin/bash
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic -y
python manage.py spectacular --file schema.yml


#python manage.py runserver
