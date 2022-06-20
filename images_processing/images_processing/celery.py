import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'images_processing.settings')

# redis_url = 'redis://localhost:6379/0'
app = Celery('images_processing')
app.control.purge()

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()