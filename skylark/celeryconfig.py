from django.conf import settings
from kombu import Queue


redis_host = settings.REDIS.get('HOST')
redis_port = settings.REDIS.get('PORT')


def get_task_queues():
    queues = []
    for item in settings.CELERY_TASK_CONF:
        queue_info = Queue(
            item.get('queue')
        )
        queues.append(queue_info)
    return tuple(queues)


def get_task_routes():
    routes = {}
    for item in settings.CELERY_TASK_CONF:
        queue_info = {
            'queue': item.get('queue')
        }
        for task in item.get('tasks'):
            routes[task] = queue_info
    return routes


# Celery config
imports = settings.CELERY_TASKS_IMPORTS
broker_url = f'redis://{redis_host}:{redis_port}/0'
result_backend = f'redis://{redis_host}:{redis_port}/0'
beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
default_queue = 'default'
# register queue
task_queues = get_task_queues()
# register task
task_routes = get_task_routes()
# register periodic task
beat_schedule = settings.CELERY_PERIOD_TASKS
# notify mq message is consumed only task finish, notifier not need
ack_late = False
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
task_ignore_result = True
# disable prefetch task, default 4
# worker_prefetch_multiplier = 1
# worker concurrency num
worker_concurrency = 2
# max execute task num will die
worker_max_tasks_per_child = 1000


