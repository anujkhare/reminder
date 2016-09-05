# Never forget your name!

## Retries
We ensure that the message is re-scheduled in case Twilio returns "failed" or
"un" status. Since the status arrives asynchronously, at a later time, the
message retries can occur any time after the initial message is scheduled
depending on when Twilio replies.

## Local time
Local time zone is determined using the browser's time zone. It is stored the
first time a user creates an account.
We could have determined the time zone using the Phone number of the user as
well. But that seemed like an unnecessary step for this task.

Packages used:
- Flask
- SQLAlchemy
- Twilio
- Celery
