# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
from twilio.rest.exceptions import TwilioRestException

# Find these values at https://twilio.com/user/account
try:
    with open('twilio_auth.txt', 'r') as f:
        account_sid = f.readline().strip('\n')
        auth_token = f.readline().strip('\n')
        twilio_phone_number = f.readline().strip('\n')
except IOError:
    print('Provide "twilio_auth.txt" with sid and token in separate lines')
    raise()

print(account_sid)
print(auth_token)
phone_number = "+91239912391239"

client = TwilioRestClient(account_sid, auth_token)

for num_try in range(1, 4):
    try:
        print('message!')
        # message = client.messages.create(to=phone_number,
        #                                  from_=twilio_phone_number,
        #                                  body="Hello there!")
        # Push this message id into some queue. Then, get the
        # You need a StatusCallback to see if the message was "sent" to carrier
        # network. We assume the status "sent" to be a success, and do not
        # actually check for delivery, as that
    except TwilioRestException:
        continue
    else:
        print('The message was sent in try {0}'.format(num_try))
        break

else:
    print('The message could not be sent in {0} tries'.format(num_try))

print('Done!')
