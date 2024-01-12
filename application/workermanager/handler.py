from django.conf import settings
from application.workermanager.models import WorkerManager
from skylark.celeryapp import app


def notify_worker_update_library():
    _notify_worker('git')


def notify_worker_stop_task(task_ids):
    _notify_worker('stop', task_ids)


def _notify_worker(cmd, *args):
    worker_queryset = WorkerManager.objects.filter(
        alive=True
    )
    for item in worker_queryset.iterator():
        app.send_task(
            settings.COMMAND_TASK,
            queue=item.queue,
            args=(cmd, *args)
        )
