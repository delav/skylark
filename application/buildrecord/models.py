from django.db import models

# Create your models here.


class BuildRecord(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    desc = models.TextField(default='', help_text='build record desc')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    create_by = models.CharField(max_length=255, help_text='create user')
    plan_id = models.IntegerField(default=None, blank=True, null=True, help_text='associated build plan')
    project_id = models.IntegerField(help_text='associated project')
    branch = models.CharField(max_length=255, help_text='project branch')
    envs = models.CharField(max_length=255, help_text='associated env id list')
    regions = models.CharField(max_length=255, default=None, blank=True, null=True,
                               help_text='associated region id list')
    periodic = models.BooleanField(default=False, help_text='if periodic task')
    status = models.IntegerField(default=0, help_text='build status,0:running, 1:finish')

    class Meta:
        verbose_name = 'build record'
        verbose_name_plural = verbose_name
        db_table = 'build_record'
