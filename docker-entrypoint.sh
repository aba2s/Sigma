#!/bin/bash

until cd /sigma/
do
    echo "--> Waiting for server volume..."
done

echo "--> Detecting database changes..."
python manage.py makemigrations sigma_app accounts

echo "--> Appliying database migration for default db..."
python manage.py migrate

echo "--> Loading batch name data..."
python manage.py loaddata batchs.json

echo "--> Collecting static files..."
python manage.py collectstatic --noinput

# echo "--> Scheduling background tasks"
# python manage.py scheduler

echo "--> Starting server"
python manage.py runserver 0.0.0.0:8000