from croniter import croniter
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class PeriodicHandler(object):

    CRONTAB_TYPE = 0
    INTERVAL_TYPE = 1

    def __init__(self, periodic_expr=''):
        self.periodic_expr = periodic_expr
        self.periodic_type = self.get_periodic_type()

    def get_periodic_type(self):
        if len(self.periodic_expr.split()) != 5:
            self.validate_interval(self.periodic_expr)
            return self.INTERVAL_TYPE
        try:
            croniter(self.periodic_expr)
        except Exception:
            raise ValueError('Invalid crontab expr')
        return self.CRONTAB_TYPE

    def save_task(self, task_name, task, task_args, queue, routing_key):
        kwargs = self._get_schedule_kwargs()
        return self.create_periodic_task(task_name, task, task_args, queue, routing_key, kwargs)

    def _get_schedule_kwargs(self):
        kwargs = {}
        if self.periodic_type == self.CRONTAB_TYPE:
            cron = croniter(self.periodic_expr)
            values = cron.expanded
            kwargs = {
                'minute': values[0][0],
                'hour': values[1][0],
                'day_of_week': values[2][0],
                'day_of_month': values[3][0],
                'month_of_year': values[4][0],
            }
        elif self.periodic_type == self.INTERVAL_TYPE:
            values = self.periodic_expr.split()
            kwargs = {
                'every': int(values[0].strip()),
                'period': values[1].strip()
            }
        return kwargs

    def create_periodic_task(self, name, task, args, queue, routing_key, schedule_kwargs):
        periodic_kwargs = {'name': name, 'task': task, 'args': args, 'queue': queue, 'routing_key': routing_key}
        if self.periodic_type == self.CRONTAB_TYPE:
            periodic_kwargs['crontab'], _ = CrontabSchedule.objects.get_or_create(
                defaults=schedule_kwargs,
                **schedule_kwargs
            )
        elif self.periodic_type == self.INTERVAL_TYPE:
            periodic_kwargs['interval'], _ = IntervalSchedule.objects.get_or_create(
                defaults=schedule_kwargs,
                **schedule_kwargs
            )
        periodic = PeriodicTask.objects.create(**periodic_kwargs)
        periodic.save()
        return periodic.id

    @staticmethod
    def validate_interval(interval_str):
        periods = ('days', 'hours', 'minutes', 'seconds', 'microseconds')
        str_list = interval_str.split()
        if len(str_list) != 2:
            raise ValueError('Invalid interval expr')
        if not str_list[0].strip().isdigit():
            raise ValueError('Invalid interval expr')
        if not str_list[1].strip().lower() in periods:
            raise ValueError('Invalid interval expr')


def get_periodic_task(task_name):
    try:
        task = PeriodicTask.objects.get(name=task_name)
    except (Exception,):
        return {}
    periodic_data = {
        'id': task.id,
        'name': task.name,
        'total_run': task.total_run_count,
        'last_run_at': str(task.last_run_at).replace('T', '')[:-7],
        'status': task.enabled,
    }
    return periodic_data


def able_task(task_name, switch):
    try:
        task = PeriodicTask.objects.get(name=task_name)
        task.enabled = switch
        task.save()
    except (Exception,):
        return False
    return True


def remove_task(task_name):
    try:
        task = PeriodicTask.objects.get(name=task_name)
        task.delete()
    except (Exception,):
        return False
    return True
