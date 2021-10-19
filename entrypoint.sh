#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py import_csv

crontab -l > mycron
echo "*/30 * * * * /usr/bin/python3 /usr/src/app/manage.py dumps_log" >> mycron
crontab mycron

python manage.py runserver

