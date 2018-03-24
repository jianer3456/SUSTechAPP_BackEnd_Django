#!/bin/sh
sudo pgrep python | xargs kill -s 9
python manage.py makemigrations
python manage.py migrate
