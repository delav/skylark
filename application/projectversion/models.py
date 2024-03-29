from django.db import models

# Create your models here.


class ProjectVersion(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    project_id = models.IntegerField(help_text='associated project')
    branch = models.CharField(max_length=255, help_text='project branch')
    total_case = models.IntegerField(default=0, help_text='branch total case')
    create_by = models.CharField(max_length=255, help_text='create user')
    update_by = models.CharField(max_length=255, help_text='update user')
    version = models.CharField(default='1.0.0', max_length=255, help_text='version')
    run_data = models.TextField(help_text='run data for build')
    sources = models.TextField(help_text='project source data')
    nodes = models.TextField(help_text='project tree nodes for front')
    remark = models.TextField(help_text='commit remark')
    status = models.IntegerField(default=0, help_text='module status')

    class Meta:
        verbose_name = 'project version'
        verbose_name_plural = verbose_name
        db_table = 'project_version'
