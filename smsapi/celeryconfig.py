BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = "redis://localhost:6379"

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'add-every-10-seconds': {
        'task': 'tasks.sms_list_data',
        'schedule': timedelta(seconds=10),
    },
   
}