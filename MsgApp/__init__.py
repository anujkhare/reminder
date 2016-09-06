import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from twilio.rest import TwilioRestClient
import datetime

from MsgApp.celery_flask import make_celery
from MsgApp.secret import install_secret_key

app = Flask(__name__, static_url_path='', static_folder='')
app.config.from_object('MsgApp.appconfig')
app.secret_key = os.environ['SECRET_KEY']
db = SQLAlchemy(app)
Session(app)
celery = make_celery(app)

twilio_account_sid  = os.environ['twilio_account_sid']
twilio_auth_token   = os.environ['twilio_auth_token']
twilio_phone_number = os.environ['twilio_phone_number']

client = TwilioRestClient(twilio_account_sid, twilio_auth_token)
VALID_HOUR_MIN = 6
VALID_HOUR_MAX = 23
LOG_FILE = 'logs/{0}.log'

from MsgApp import models, views, tasks
