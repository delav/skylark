from celery import Celery

app = Celery('worker', include=['worker.tasks'])
app.config_from_object('worker.config', namespace='CELERY')
