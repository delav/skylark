from django.db import models

# Create your models here.


class Environment(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    env_name = models.CharField(max_length=255, help_text='environment name')

    class Meta:
        verbose_name = 'environment'
        verbose_name_plural = verbose_name
        db_table = 'environment'
