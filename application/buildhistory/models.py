from django.db import models
from application.buildplan.models import BuildPlan

# Create your models here.


class BuildHistory(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    total_case = models.IntegerField(default=0, blank=True, help_text='total cases number')
    failed_case = models.IntegerField(default=0, blank=True, help_text='failed cases number')
    passed_case = models.IntegerField(default=0, blank=True, help_text='passed cases number')
    skipped_case = models.IntegerField(default=0, blank=True, help_text='skipped cases number')
    create_at = models.DateTimeField(auto_now_add=True, help_text='build time')
    start_time = models.DateTimeField(default=None, blank=True, null=True, help_text='task start time')
    end_time = models.DateTimeField(default=None, blank=True, null=True, help_text='task end time')
    build_plan = models.ForeignKey(BuildPlan, on_delete=models.DO_NOTHING, help_text='associated build plan')
    status = models.IntegerField(default=-1, help_text='build status,-1:waiting, 0:normal, 1:abnormal')
    task_id = models.CharField(default=None, null=True, max_length=255, help_text='celery task id')
    report_path = models.CharField(default='', max_length=255, help_text='build report path')

    class Meta:
        verbose_name = 'build history'
        verbose_name_plural = verbose_name
        db_table = 'build_history'
