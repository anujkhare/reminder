from twilio.rest.exceptions import TwilioRestException

from MsgApp import celery, datetime
from MsgApp.models import UserData
from MsgApp import twilio_phone_number, client
from MsgApp import VALID_HOUR_MIN, VALID_HOUR_MAX, LOG_FILE


@celery.task
def send_sms(user, time_initiated):
    ''' Sends an sms to "user.phone" containing "user.name".
    '''
    logfile = open(LOG_FILE.format(user.name), 'a')
    timestamp = str(time_initiated.replace(microsecond=0))
    for num_try in range(1, 4):
        try:
            print(' '.join(['message! to', str(user.phone), user.name]))
            body = ''.join(['Hi! Your name is ', user.name,
                            '. Sent using "Name Reminder"!'])
            message = client.messages.create(to=user.phone,
                                             from_=twilio_phone_number,
                                             body=body)
            print(message)
            # Push this message id into some queue. Then, get the
            # You need a StatusCallback to see if the message was "sent"
            # to carrier
            # network. We assume the status "sent" to be a success, and do not
            # actually check for delivery, as that
        except TwilioRestException as e:
            logfile.write(''.join([timestamp, ': ', str(e), '\n']))
            print(e)
            continue
        else:
            msg = 'The message was sent in try {0}'.format(num_try)
            print(msg)
            logfile.write(''.join([timestamp, ': ', msg, '\n']))
            break

    else:
        msg = 'The message could not be sent in {0} tries'.format(num_try)
        print(msg)
        logfile.write(''.join([timestamp, ': ', msg, '\n']))
    logfile.close()


# This task is scheduled to run every minute, since different time zones will
# clock hours at different times.
# Not very efficient, but this will work just fine for our small use case.
@celery.task
def check_and_schedule_sms():
    ''' Checks if the local time for a given user is within the VALID range,
        and if it is exactly an hour (ab:00:xy), and schedules a message to be
        sent.
    '''
    time_utc = datetime.datetime.utcnow()
    for user in UserData.query.all():
        print(user)
        time_local = time_utc - datetime.timedelta(minutes=user.tz_offset)
        if is_message_time(time_local):
            send_sms.delay(user, time_local)


def is_message_time(time_local):
    ''' Checks if the given time is within the VALID range,
        and if it is exactly an hour (ab:00:xy).
    '''
    # print(time_local.hour)
    # print(time_local.minute)
    # if time_local.minute != 0:
    #     print('NOT 0 abhi!')
    #     return False
    if VALID_HOUR_MIN > time_local.hour or time_local.hour > VALID_HOUR_MAX:
        print('NOT a valid hour!')
        return False

    return True
