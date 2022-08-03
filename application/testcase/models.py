from django.db import models
from application.user.models import User
from application.testsuite.models import TestSuite
from application.casetag.models import CaseTag
from application.casepriority.models import CasePriority

# Create your models here.


class TestCase(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    case_name = models.CharField(max_length=255, help_text='test case name')
    case_desc = models.TextField(default=None, blank=True, null=True, help_text='test case desc')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    update_by = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, help_text='last update user')
    case_pri = models.ForeignKey(CasePriority, related_name='pri', null=True, on_delete=models.SET_NULL,
                                 help_text='test case priority')
    case_tag = models.ManyToManyField(CaseTag, related_name='tags', blank=True, help_text='test case tags')
    test_suite = models.ForeignKey(TestSuite, related_name='cases', null=True, on_delete=models.CASCADE,
                                   help_text='associated test suite')
    case_type = models.IntegerField(default=0, choices=((0, 'T0'), (1, 'T1')),
                                    help_text='case type, 0: normal test case; 1:use customize keyword')
    inputs = models.TextField(default=None, blank=True, null=True, help_text='input args for keyword')
    outputs = models.TextField(default=None, blank=True, null=True, help_text='output args for keyword')
    timeout = models.CharField(default=None, max_length=255, blank=True, null=True, help_text='case timeout')
    deleted = models.BooleanField(default=1, help_text='if deleted')

    class Meta:
        verbose_name = 'test case'
        verbose_name_plural = verbose_name
        db_table = 'test_case'
        ordering = ['create_at']
        unique_together = ['case_name', 'test_suite']