from django.db import models
from application.user.models import User

# Create your models here.


class ProjectVersion(models.Model):
    
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    branch = models.CharField(default=None, max_length=255, blank=True, null=True, help_text='project branch')
    create_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                                  related_name='version_user', help_text='create user')
    version = models.CharField(default=None, max_length=255, blank=True, null=True, help_text='project version')
    content = models.TextField(help_text='project data')

    class Meta:
        verbose_name = 'project version'
        verbose_name_plural = verbose_name
        db_table = 'project_version'
