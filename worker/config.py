from kombu import Queue, Exchange


# Redis
REDIS = {
    'HOST': 'localhost',
    'PORT': '6379',
    'PASSWORD': '',
}
# Run case result
ROBOT_REDIS_URL = f'redis://{REDIS.get("HOST")}/1'

# Celery config
BROKER_URL = f'redis://{REDIS.get("HOST")}/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS.get("HOST")}/0'
CELERY_QUEUES = (
    Queue('robot_runner', Exchange('robot_runner'), routing_key='runner'),
    Queue('robot_reporter', Exchange('robot_reporter'), routing_key='reporter'),
 )
CELERY_ROUTES = {
    'worker.runner.tasks.robot_runner': {'queue': 'robot_runner', 'routing_key': 'runner'},
    'worker.runner.tasks.merge_report': {'queue': 'robot_reporter', 'routing_key': 'reporter'},
 }
# data type of task accept
CELERY_ACCEPT_CONTENT = ['json']
# serialize type
CELERY_TASK_SERIALIZER = 'json'
# timezone
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
# task timeout
CELERY_TASK_RESULT_EXPIRES = 60*60*24
# disable prefetch task, default 4
CELERYD_PREFETCH_MULTIPLIER = 1
# worker concurrency num
# CELERYD_CONCURRENCY = 3
# max execute task num will die
# CELERYD_MAX_TASKS_PER_CHILD = 100
