import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skylark.settings')
app = Celery('skylark')
app.config_from_object('skylark.celeryconfig')
app.autodiscover_tasks()
