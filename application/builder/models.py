from django.db import models
from application.user.models import User
from application.project.models import Project
from application.environment.models import Environment

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
                                 help_text='build status,-1:waiting,0:normal,1:abnormal')
    cron_job = models.BooleanField(default=False, help_text='if timing task')
    build_data = models.TextField(default=None, blank=True, null=True, help_text='build data')
    debug = models.BooleanField(default=True, help_text='if debug')
    task_id = models.CharField(default=None, null=True, max_length=128, help_text='celery task id')
    env = models.ForeignKey(Environment, help_text='associated env', on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, help_text='associated project', on_delete=models.DO_NOTHING)
    report_path = models.CharField(default='', max_length=256, help_text='report path')

    class Meta:
        verbose_name = 'builder'
        verbose_name_plural = verbose_name
        db_table = 'builder'
