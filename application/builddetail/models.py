from django.db import models
from application.builder.models import Builder
from application.testcase.models import TestCase

# Create your models here.


class BuildDetail(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    test_case = models.ForeignKey(TestCase, null=True, on_delete=models.DO_NOTHING, help_text='associated case')
    start_time = models.DateTimeField(null=True, blank=True, help_text='run start time')
    end_time = models.DateTimeField(null=True, blank=True, help_text='run end time')
    result = models.CharField(default=None, max_length=64, null=True, help_text='PASS, FAIL, SKIP')
    builder = models.ForeignKey(Builder, null=True, on_delete=models.CASCADE, help_text='associated build')

    class Meta:
        verbose_name = 'build detail'
        verbose_name_plural = verbose_name
        db_table = 'buidl_detail'
