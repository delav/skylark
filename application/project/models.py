from django.db import models

# Create your models here.


class Project(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(unique=True, max_length=255, help_text='project name')
    create_at = models.DateTimeField(auto_now_add=True,  help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    create_by = models.CharField(max_length=255, help_text='create user')
    update_by = models.CharField(max_length=255, help_text='last update user')
    group_id = models.IntegerField(help_text='belong to group or team')
    status = models.IntegerField(default=0, help_text='module status')
    personal = models.BooleanField(default=False, help_text='personal project')

    class Meta:
        verbose_name = 'project'
        verbose_name_plural = verbose_name
        db_table = 'project'
        ordering = ['create_at']