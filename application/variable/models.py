from django.db import models
from django.conf import settings
from application.environment.models import Environment

# Create your models here.


class Variable(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    module_id = models.IntegerField(help_text='associated module id')
    module_type = models.IntegerField(default=0, choices=settings.MODULE_TYPE, help_text='associated module type')
    name = models.CharField(max_length=255, help_text='variable name')
    value = models.TextField(null=True, blank=True, help_text='variable value')
    value_type = models.IntegerField(default=0, choices=settings.VALUE_TYPE, help_text='variable value type')
    env = models.ForeignKey(Environment, null=True, related_name='envs', on_delete=models.CASCADE,
                            help_text='associated environment')
    seq_number = models.IntegerField(default=None, null=True, help_text='variable sequence number')
    edit = models.BooleanField(default=False, help_text='variable if can edit')
    remark = models.TextField(null=True, blank=True, help_text='remark')

    class Meta:
        verbose_name = 'variable'
        verbose_name_plural = verbose_name
        db_table = 'variable'
