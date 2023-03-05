from django.db import models
from application.testsuite.models import TestSuite
from application.environment.models import Environment

# Create your models here.


class VirtualFile(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    env = models.ForeignKey(Environment, null=True, on_delete=models.CASCADE, help_text='associated environment')
    file_subfix = models.CharField(default=None, blank=True, null=True, max_length=255, help_text='file subfix name')
    file_text = models.TextField(default=None, blank=True, null=True, help_text='file content')
    test_suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE, help_text='associated suite')
    remark = models.TextField(default=None, blank=True, null=True, help_text='remark')

    class Meta:
        verbose_name = 'virtual file'
        verbose_name_plural = verbose_name
        db_table = 'virtual_file'
