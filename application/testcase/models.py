from django.db import models
from application.testsuite.models import TestSuite
from application.casepriority.models import CasePriority

# Create your models here.


class TestCase(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(max_length=255, help_text='test case name')
    category = models.IntegerField(default=0, help_text='model category')
    document = models.TextField(default=None, blank=True, null=True, help_text='test case desc')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    create_by = models.CharField(max_length=255, help_text='create user')
    update_by = models.CharField(max_length=255, help_text='last update user')
    priority_id = models.IntegerField(default=None, null=True, blank=True, help_text='test case priority')
    test_suite = models.ForeignKey(TestSuite, related_name='cases', on_delete=models.CASCADE,
                                   help_text='associated test suite')
    order = models.IntegerField(default=None, blank=True, null=True, help_text='execute order in suite')
    project_id = models.IntegerField(help_text='associated project')
    inputs = models.TextField(default=None, blank=True, null=True, help_text='input args for keyword')
    outputs = models.TextField(default=None, blank=True, null=True, help_text='output args for keyword')
    timeout = models.CharField(default=None, max_length=255, blank=True, null=True, help_text='case timeout')
    status = models.IntegerField(default=0, help_text='test case status')

    class Meta:
        verbose_name = 'test case'
        verbose_name_plural = verbose_name
        db_table = 'test_case'
        unique_together = ('name', 'test_suite')