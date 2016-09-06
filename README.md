# Never forget your name!
[See this in action on Heroku!](http://cryptic-wildwood-57006.herokuapp.com/)

## Todos
- use nginx for concurrent connections

## Function
Allows users to enter their name and phone number, and sends an hourly message
in 'day hours' to their phone containing their name.
Logs the message activity and allows users to view the logs.

Uses Twilio to send messages. Can only send messages to *verified numbers*.

## Instructions to run
For a simpler setup with docker, use [this repository](https://github.com/anujkhare/reminder_docker).
- Start Redis and Postgresql
- Set the following env vars:
```
SECRET_KEY
REDIS_UR
DATABASE_URL
PORT
twilio_account_sid
twilio_auth_token
twilio_phone_number
```
- bash run_web.sh
- bash run_celery.sh

## Storage
Sessions maintained on Redis. For celery, broker and messege queue on Redis.
Logs and user data stored on PostgreSQL.

## Retries
We ensure that the message is re-scheduled in case Twilio returns "failed" or "un" status through it's StatusCallback. Since the status arrives asynchronously, at a later time, the message retries can occur any time after the initial message is scheduled depending on when Twilio replies.

## Local time
Local time zone is determined using the browser's time zone. It is stored the
first time a user creates an account.
We could have determined the time zone using the Phone number of the user as
well. But that seemed like an unnecessary step for this task.

## Packages used:
See requirements.txt

- Flask
- celery
- postgresql
- redis
