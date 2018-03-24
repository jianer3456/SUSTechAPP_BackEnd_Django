#!/bin/sh
sudo pgrep python | xargs kill -s 9
python manage.py runserver 0.0.0.0:4000

