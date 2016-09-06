#!/bin/sh

echo 'Hi there!'
# migrate db, so we have the latest db schema
# su -m kcm -c "python manage.py db init"
# su -m kcm -c "python manage.py db migrate"  
python manage.py db upgrade
# start development server on public ip interface, on port 3000 (or PORT)
python MsgApp/runserver.py
