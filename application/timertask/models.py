from django.db import models


class TimerTask(models.Model):
    
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    timer_str = models.TextField(help_text='date time expression')
    status = models.BooleanField(default=True, help_text='1: open 0: closed')
    timer_type = models.IntegerField(default=0, choices=((0, 'crontab'), (1, 'interval')),
                                     help_text='0: crontab type, 1: interval type')
    periodic_ids = models.TextField(default=None, blank=True, null=True, help_text='periodic task ids')

    class Meta:
        verbose_name = 'timer task'
        verbose_name_plural = verbose_name
        db_table = 'timer_task'
