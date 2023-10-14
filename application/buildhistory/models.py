from django.db import models

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
    record_id = models.IntegerField(help_text='associated build record')
    env_id = models.IntegerField(help_text='associated environment')
    region_id = models.IntegerField(default=None, blank=True, null=True, help_text='associated region')
    status = models.IntegerField(default=-1, help_text='build status')
    batch = models.IntegerField(default=1, help_text='task batch number')
    celery_task = models.CharField(default=None, null=True, max_length=255, help_text='celery task id')
    report_path = models.CharField(default='', max_length=255, help_text='build report path')

    class Meta:
        verbose_name = 'build history'
        verbose_name_plural = verbose_name
        db_table = 'build_history'


class HistoryDetail(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    case_id = models.IntegerField(help_text='associated case')
    start_time = models.DateTimeField(null=True, blank=True, help_text='run start time')
    end_time = models.DateTimeField(null=True, blank=True, help_text='run end time')
    result = models.CharField(default=None, max_length=64, blank=True, null=True, help_text='PASS, FAIL, SKIP')
    history_id = models.IntegerField(help_text='associated build history')

    class Meta:
        verbose_name = 'history detail'
        verbose_name_plural = verbose_name
        db_table = 'history_detail'
