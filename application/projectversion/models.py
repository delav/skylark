from django.db import models

# Create your models here.


class ProjectVersion(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    project_id = models.IntegerField(help_text='associated project')
    branch = models.CharField(max_length=255, help_text='project branch')
    create_by = models.CharField(max_length=255, help_text='create user')
    update_by = models.CharField(max_length=255, help_text='update user')
    version = models.CharField(default=None, null=True, blank=True, max_length=255, help_text='project version')
    content = models.TextField(help_text='project tree data')
    sources = models.TextField(help_text='project source data')
    remark = models.TextField(help_text='commit remark')
    status = models.IntegerField(default=0, help_text='version status')

    class Meta:
        verbose_name = 'project version'
        verbose_name_plural = verbose_name
        db_table = 'project_version'
