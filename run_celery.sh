#!/bin/sh

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
celery -A MsgApp.celery worker --loglevel=info --beat
