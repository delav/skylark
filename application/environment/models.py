from django.db import models

# Create your models here.


class Environment(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(max_length=255, help_text='environment name')
    default = models.BooleanField(default=False, help_text='if default')

    class Meta:
        verbose_name = 'environment'
        verbose_name_plural = verbose_name
        db_table = 'environment'
