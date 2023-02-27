from croniter import croniter
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class DynamicTimer(object):

    CRONTAB_TYPE = 0
    INTERVAL_TYPE = 1

    def __init__(self, timer_str, timer_type=0):
        self.timer_str = timer_str
        self.timer_type = timer_type

    def save_task(self, task_name, task, task_args, queue, routing_key):
        kwargs = self._get_schedule_kwargs()
        return self.create_periodic_task(task_name, task, task_args, queue, routing_key, kwargs)

    def _get_schedule_kwargs(self):
        kwargs = {}
        if self.timer_type == self.CRONTAB_TYPE:
            cron = croniter(self.timer_str)
            values = cron.expanded
            kwargs = {
                'minute': values[0][0],
                'hour': values[1][0],
                'day_of_week': values[2][0],
                'day_of_month': values[3][0],
                'month_of_year': values[4][0],
            }
        elif self.timer_type == self.INTERVAL_TYPE:
            values = self.handle_interval_str(self.timer_str)
            kwargs = {
                'every': values[0],
                'period': values[1]
            }
        return kwargs

    def create_periodic_task(self, name, task, args, queue, routing_key, schedule_kwargs):
        periodic_kwargs = {'name': name, 'task': task, 'args': args, 'queue': queue, 'routing_key': routing_key}
        if self.timer_type == self.CRONTAB_TYPE:
            periodic_kwargs['crontab'] = CrontabSchedule.objects.get_or_create(
                defaults=schedule_kwargs,
                **schedule_kwargs
            )
        elif self.timer_type == self.INTERVAL_TYPE:
            periodic_kwargs['interval'] = IntervalSchedule.objects.get_or_create(
                defaults=schedule_kwargs,
                **schedule_kwargs
            )
        periodic = PeriodicTask.objects.create(**periodic_kwargs)
        periodic.save()
        return periodic.id

    def handle_interval_str(self, interval_str):
        values = [60, 'seconds']
        periods = ('days', 'hours', 'minutes', 'seconds', 'microseconds')
        str_list = interval_str.split()
        if len(str_list) != 2:
            return values
        if str_list[0].isdigit():
            values[0] = int(str_list[0])
        if str_list[1].lower() in periods:
            values[1] = str_list[1]
        return values

    def get_periodic_task(self, task_name):
        periodic = []
        try:
            task = PeriodicTask.objects.filter(name=task_name).select_related('interval', 'crontab')
        except (Exception,):
            return {}
        if self.timer_type == self.CRONTAB_TYPE:
            periodic = [
                task.crontab.minute, task.crontab.hour, task.crontab.day_of_week,
                task.crontab.day_of_month, task.crontab.month_of_year
            ]
        elif self.timer_type == self.INTERVAL_TYPE:
            periodic = [
                'every', str(task.interval.every), task.interval.period
            ]
        periodic_data = {
            'id': task.id,
            'name': task.name,
            'total_run': task.total_run_count,
            'last_run_at': str(task.last_run_at).replace('T', '')[:-7],
            'status': task.enabled,
            'timer_str': ' '.join(periodic),
        }
        return periodic_data

    def able_task(self, task_name, switch):
        try:
            task = PeriodicTask.objects.get(name=task_name)
            task.enabled = switch
            task.save()
        except (Exception,):
            return False
        return True

    def remove_task(self, task_name):
        try:
            task = PeriodicTask.objects.get(name=task_name)
            task.delete()
        except (Exception,):
            return False
        return True
