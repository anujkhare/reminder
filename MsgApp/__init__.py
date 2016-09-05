from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from twilio.rest import TwilioRestClient
import datetime

from MsgApp.celery_flask import make_celery
from MsgApp.secret import install_secret_key

app = Flask(__name__, static_url_path='', static_folder='')
app.config.from_object('MsgApp.appconfig')
app.secret_key = 'asd fasdf sdfsafaerwdvaeqwfsawefasdfawefawefawefaw'
print(app.config['SECRET_KEY'])
install_secret_key(app)
db = SQLAlchemy(app)
Session(app)
celery = make_celery(app)

try:
    with open('twilio_auth.txt', 'r') as f:
        twilio_account_sid = f.readline().strip('\n')
        twilio_auth_token = f.readline().strip('\n')
        twilio_phone_number = f.readline().strip('\n')
except IOError:
    print('Provide "twilio_auth.txt" with sid and token in separate lines')
    raise(IOError)

client = TwilioRestClient(twilio_account_sid, twilio_auth_token)
VALID_HOUR_MIN = 6
VALID_HOUR_MAX = 23
LOG_FILE = 'logs/{0}.log'

from MsgApp import models, views, tasks
