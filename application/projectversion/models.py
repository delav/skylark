from django.db import models
from application.user.models import User
from application.project.models import Project

# Create your models here.


class ProjectVersion(models.Model):
    
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    project = models.ForeignKey(Project, related_name='versions', on_delete=models.CASCADE,
                                help_text='associated project')
    branch = models.CharField(max_length=255, help_text='project branch')
    create_by = models.ForeignKey(User, blank=True, null=True, related_name='version_cuser',
                                  on_delete=models.DO_NOTHING, help_text='create user')
    update_by = models.ForeignKey(User, blank=True, null=True, related_name='version_muser',
                                  on_delete=models.DO_NOTHING, help_text='update user')
    version = models.CharField(default='1.0.0', max_length=255, help_text='project version')
    content = models.TextField(help_text='project tree data')
    sources = models.TextField(help_text='project source data')
    remark = models.TextField(help_text='commit remark')
    deleted = models.BooleanField(default=0, help_text='if deleted')

    class Meta:
        verbose_name = 'project version'
        verbose_name_plural = verbose_name
        db_table = 'project_version'
