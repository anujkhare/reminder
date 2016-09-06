import datetime
from MsgApp import db


class UserData(db.Model):
    name = db.Column(db.String(80), unique=True, primary_key=True)
    phone = db.Column(db.String(13), unique=True, default='', primary_key=True)
    start_time = db.Column(db.DateTime, unique=False)
    tz_offset = db.Column(db.Integer, unique=False, default=0)

    def __init__(self, name, phone, start_time, tz_offset):
        self.name = name
        self.phone = phone
        # time is UTC
        self.start_time = start_time
        # offset (UTC - localTimeZone) MINUTES
        self.tz_offset = tz_offset

    def __repr__(self):
        return '<User {0}>'.format(self.name)

    def get_local_start_time(self):
        timediff = datetime.timedelta(minutes=self.tz_offset)
        return self.start_time - timediff


class UserLogs(db.Model):
    """ Implementing logs in a single SQL table, because Heroku uses ephemeral
        storage making write to disk files for logs unstable. Find better way?
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    log = db.Column(db.VARCHAR)

    def __init__(self, name, log):
        self.name = name
        self.log = log

    def __repr__(self):
        return '{}'.format(self.log)
