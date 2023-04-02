from django.db import models
from application.user.models import User
from application.project.models import Project
from django_celery_beat.models import PeriodicTask

# Create your models here.


class BuildPlan(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    title = models.TextField(default='', help_text='buidl title')
    total_case = models.IntegerField(default=0, help_text='total cases number')
    create_at = models.DateTimeField(auto_now_add=True, help_text='build time')
    update_at = models.DateTimeField(auto_now=True, help_text='last update time')
    create_by = models.ForeignKey(User,  related_name='build_cuser',
                                  on_delete=models.DO_NOTHING, help_text='create user')
    update_by = models.ForeignKey(User, related_name='build_muser',
                                  on_delete=models.DO_NOTHING, help_text='last update user')
    build_cases = models.TextField(default='',  help_text='build case id list')
    periodic_expr = models.CharField(default='', help_text='periodic expr')
    periodic_task = models.ForeignKey(PeriodicTask, null=True, blank=True,
                                      on_delete=models.SET_NULL, help_text='associated periodic task')
    periodic_switch = models.BooleanField(default=False, help_text='periodic task switch')
    envs = models.CharField(max_length=255, help_text='associated env id list')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, help_text='associated project')
    branch = models.CharField(max_length=255, help_text='project branch')
    expect_pass = models.FloatField(default=1.0, help_text='expected pass rate')
    extra_data = models.TextField(default='{}',  help_text='build extra data of json')

    class Meta:
        verbose_name = 'build plan'
        verbose_name_plural = verbose_name
        db_table = 'build_plan'
