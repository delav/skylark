from django.db import models

# Create your models here.


class ExecuteParam(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    create_at = models.DateTimeField(auto_now_add=True, help_text='build time')
    update_at = models.DateTimeField(auto_now=True, help_text='last update time')
    create_by = models.CharField(max_length=255, help_text='create user')
    update_by = models.CharField(max_length=255, help_text='last update user')
    parameters = models.TextField(default='', help_text='parameters')
    project_id = models.IntegerField(help_text='related project')
    remark = models.TextField(default=None, null=True, blank=True, help_text='remark')

    class Meta:
        verbose_name = 'execute param'
        verbose_name_plural = verbose_name
        db_table = 'execute_param'

