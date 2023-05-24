from celery import Celery
import os
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SubtitleTimeTracker.settings')

CELERY_BROKER_URL = f'amqp://{os.environ.get("RABBITMQ_DEFAULT_USER")}:{os.environ.get("RABBITMQ_DEFAULT_PASS")}@rabbit//'
# CELERY_BROKER_URL = 'amqp://localhost'
# CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite3'  # Replace with the URL of your result backend (e.g., a database)
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'

app = Celery('spinnyWorker', broker=CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
