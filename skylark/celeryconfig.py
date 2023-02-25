from django.conf import settings
from kombu import Queue


redis_host = settings.REDIS.get('HOST')
redis_port = settings.REDIS.get('PORT')

# Celery config
imports = settings.CELERY_TASKS_PATH
broker_url = f'redis://{redis_host}:{redis_port}/0'
result_backend = f'redis://{redis_host}:{redis_port}/0'
task_queues = (
    Queue(settings.NOTIFIER_QUEUE, routing_key=settings.NOTIFIER_ROUTING_KEY),
 )
task_routes = {
    settings.NOTIFIER_TASK: {'queue': settings.NOTIFIER_QUEUE, 'routing_key': settings.NOTIFIER_ROUTING_KEY}
 }
# notify mq message is consumed only task finish, notifier not need
# ack_late = True
# data type of task accept
accept_content = ['json']
# serialize type
task_serializer = 'json'
# timezone
timezone = 'Asia/Shanghai'
enable_utc = False
# task result expire time(s)
result_expires = 60*60
# not receive ack will send to other worker
disable_rate_limits = True
# result not send to broker
# ignore_result = True
# disable prefetch task, default 4
worker_prefetch_multiplier = 1
# worker concurrency num
worker_concurrency = 2
# max execute task num will die
worker_max_tasks_per_child = 1000


