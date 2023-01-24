from datetime import datetime
from skylark.celeryapp import app
from loguru import logger
from application.builder.models import Builder


@app.task(bind=True)
def robot_runner(self, task_id, run_suite, meta_data, report_path):
    """robot execute task, no logic needed here, worker will do it"""
    pass


@app.task(bind=True)
def robot_notifier(self, task_id, **kwargs):
    try:
        if 'start_time' in kwargs:
            kwargs['start_time'] = datetime.fromtimestamp(kwargs['start_time'])
        if 'end_time' in kwargs:
            kwargs['end_time'] = datetime.fromtimestamp(kwargs['end_time'])
        Builder.objects.filter(id=task_id).update(**kwargs)
    except (Exception,) as e:
        logger.error(f'[{task_id}]notice result failed: {e}')
    # TODO


