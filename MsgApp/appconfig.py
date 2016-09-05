import os
from celery.schedules import crontab


# postgresql config:
DB_HOST = os.environ.get('DB_PORT_5432_TCP_ADDR', 'localhost')
DB_PORT = os.environ.get('DB_PORT_5432_TCP_PORT', 5432)
DB_USER = os.environ.get('DB_ENV_POSTGRES_USER', 'postgres')
DB_PASS = os.environ.get('DB_ENV_POSTGRES_PASSWORD', '')
DB_NAME = os.environ.get('DB_ENV_POSTGRES_DB', '')

POSTGRES_URL = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASS,
                                                    DB_HOST, DB_PORT,
                                                    DB_NAME)
print(POSTGRES_URL)
SQLALCHEMY_DATABASE_URI = POSTGRES_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False

# configure Redis server:
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR', '127.0.0.1')
REDIS_URL = 'redis://{}:{}/{}'.format(REDIS_HOST, REDIS_PORT, REDIS_DB)

# celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'MsgApp.tasks.check_and_schedule_sms',
        'schedule': crontab(minute='*/1'),
    },
}
