from django.db import models

# Create your models here.


class ProjectPermission(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    user_id = models.IntegerField(help_text='user id')
    project_id = models.IntegerField(help_text='project id')

    class Meta:
        verbose_name = 'project permission'
        verbose_name_plural = verbose_name
        db_table = 'project_permission'
