from django.db import models
from application.user.models import User
from application.project.models import Project
from application.environment.models import Environment
from application.timertask.models import TimerTask

# Create your models here.


class Builder(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    total_case = models.IntegerField(default=0, blank=True, help_text='total cases number')
    failed_case = models.IntegerField(default=0, blank=True, help_text='failed cases number')
    passed_case = models.IntegerField(default=0, blank=True, help_text='passed cases number')
    skipped_case = models.IntegerField(default=0, blank=True, help_text='skipped cases number')
    build_time = models.DateTimeField(auto_now_add=True, help_text='build time')
    start_time = models.DateTimeField(default=None, blank=True, null=True, help_text='task start time')
    end_time = models.DateTimeField(default=None, blank=True, null=True, help_text='task end time')
    build_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, help_text='build user')
    status = models.IntegerField(default=-1, blank=True,
                                 help_text='build status,-1:waiting, 0:normal, 1:abnormal')
    build_data = models.TextField(default=None, blank=True, null=True, help_text='build data')
    timer_task = models.ForeignKey(TimerTask, null=True, blank=True, on_delete=models.SET_NULL,
                                   help_text='associated timer task')
    debug = models.BooleanField(default=True, help_text='if debug, debug not save build detail')
    batch = models.IntegerField(default=0, help_text='task batch number')
    task_id = models.CharField(default=None, null=True, max_length=128, help_text='celery task id')
    env = models.ForeignKey(Environment, on_delete=models.DO_NOTHING, help_text='associated env')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, help_text='associated project')
    report_path = models.CharField(default='', max_length=255, help_text='report path')

    class Meta:
        verbose_name = 'builder'
        verbose_name_plural = verbose_name
        db_table = 'builder'
