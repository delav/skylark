from django.db import models
from application.builder.models import Builder

# Create your models here.


class BuildDetail(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    suite_name = models.CharField(max_length=255, help_text='test suite name')
    case_id = models.IntegerField(help_text='test case id')
    case_name = models.CharField(max_length=255, help_text='case name')
    start_time = models.DateTimeField(null=True, blank=True, help_text='run start time')
    end_time = models.DateTimeField(null=True, blank=True, help_text='run end time')
    result = models.IntegerField(default=-1, help_text='result, -1:waiting,0:failure,1:success')
    builder = models.ForeignKey(Builder, null=True, on_delete=models.CASCADE, help_text='build id')

    class Meta:
        verbose_name = 'build detail'
        verbose_name_plural = verbose_name
        db_table = 'buidl_detail'
