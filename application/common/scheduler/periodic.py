import pytz
from datetime import datetime, timedelta
from croniter import croniter
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class PeriodicHandler(object):

    CRONTAB_TYPE = 0
    INTERVAL_TYPE = 1

    def __init__(self, periodic_expr=''):
        self.periodic_expr = periodic_expr
        self.periodic_type = self._get_periodic_type()

    def create_task(self, task_name, task, task_args, queue, routing_key=None):
        kwargs = self._get_schedule_kwargs()
        return self._create_periodic_task(task_name, task, task_args, queue, routing_key, kwargs)

    def update_task(self, periodic_task_id):
        kwargs = self._get_schedule_kwargs()
        self._update_periodic_task(periodic_task_id, kwargs)

    def _get_periodic_type(self):
        if len(self.periodic_expr.split()) != 5:
            self._validate_interval(self.periodic_expr)
            return self.INTERVAL_TYPE
        valid = croniter.is_valid(self.periodic_expr)
        if not valid:
            raise ValueError('Invalid crontab expr')
        return self.CRONTAB_TYPE

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

    def _update_periodic_task(self, periodic_task_id, schedule_kwargs):
        periodic_schedule = self._get_periodic_schedule(schedule_kwargs)
        periodic = PeriodicTask.objects.get(id=periodic_task_id)
        if 'crontab' in periodic_schedule:
            periodic.crontab = periodic_schedule['crontab']
        elif 'interval' in periodic_schedule:
            periodic.interval = periodic_schedule['interval']
        periodic.save()

    def _create_periodic_task(self, name, task, args, queue, routing_key, schedule_kwargs):
        periodic_kwargs = {'name': name, 'task': task, 'args': args, 'queue': queue, 'routing_key': routing_key}
        periodic_schedule = self._get_periodic_schedule(schedule_kwargs)
        periodic_kwargs.update(periodic_schedule)
        periodic = PeriodicTask.objects.create(**periodic_kwargs)
        return periodic.id

    def _get_periodic_schedule(self, schedule_kwargs):
        periodic_schedule = {}
        if self.periodic_type == self.CRONTAB_TYPE:
            periodic_schedule['crontab'], _ = CrontabSchedule.objects.get_or_create(
                defaults=schedule_kwargs,
                **schedule_kwargs
            )
        elif self.periodic_type == self.INTERVAL_TYPE:
            periodic_schedule['interval'], _ = IntervalSchedule.objects.get_or_create(
                defaults=schedule_kwargs,
                **schedule_kwargs
            )
        return periodic_schedule

    @staticmethod
    def _validate_interval(interval_str):
        periods = ('days', 'hours', 'minutes', 'seconds', 'microseconds')
        str_list = interval_str.split()
        if len(str_list) != 2:
            raise ValueError('Invalid interval expr')
        if not str_list[0].strip().isdigit():
            raise ValueError('Invalid interval expr')
        if not str_list[1].strip().lower() in periods:
            raise ValueError('Invalid interval expr')


def get_periodic_list(**kwargs):
    result = []
    try:
        queryset = PeriodicTask.objects.filter(
            **kwargs
        ).select_related('interval', 'crontab')
    except (Exception,):
        return result
    for item in queryset.iterator():
        next_time, to_next = datetime.now(), 0
        if not item.crontab and not item.interval:
            continue
        if item.crontab:
            periodic_expr = ' '.join([
                item.crontab.minute,
                item.crontab.hour,
                item.crontab.day_of_week,
                item.crontab.day_of_month,
                item.crontab.month_of_year
            ])
            tz = pytz.timezone('Asia/Shanghai')
            local_date = tz.localize(datetime.now())
            cron = croniter(periodic_expr, local_date)
            next_timestamp = cron.get_next()
            next_time = datetime.fromtimestamp(next_timestamp)
            to_next = (next_time - datetime.now()).total_seconds()
        elif item.interval:
            every = item.interval.every
            period = item.interval.period
            if period == 'days':
                t = 60 * 60 * 24 * every
            elif period == 'hours':
                t = 60 * 60 * every
            elif period == 'minutes':
                t = 60 * every
            elif period == 'seconds':
                t = every
            else:
                t = 60 * 60
            if item.last_run_at:
                next_time = item.last_run_at + timedelta(seconds=t)
                to_next = (next_time - datetime.now().timestamp()).total_seconds()
            else:
                next_time = datetime.now() + timedelta(seconds=t)
                to_next = t
        next_time = str(next_time).replace('T', ' ')
        item_data = {
            'id': item.id,
            'name': item.name,
            'last_run_at': item.last_run_at,
            'enabled': item.enabled,
            'next_time': next_time,
            'to_next': to_next
        }
        result.append(item_data)
    return result


def get_periodic_task(**kwargs):
    try:
        task = PeriodicTask.objects.get(**kwargs)
    except (Exception,):
        return {}
    periodic_data = {
        'id': task.id,
        'name': task.name,
        'total_run': task.total_run_count,
        'last_run_at': str(task.last_run_at).replace('T', '')[:-7],
        'enabled': task.enabled,
    }
    return periodic_data


def able_task(task_id, switch):
    try:
        task = PeriodicTask.objects.get(id=task_id)
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
