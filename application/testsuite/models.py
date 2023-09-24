from django.db import models
from application.suitedir.models import SuiteDir

# Create your models here.


class TestSuite(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(max_length=255, help_text='test suite name')
    document = models.TextField(default=None, blank=True, null=True, help_text='suite desc')
    category = models.IntegerField(default=0, help_text='model category')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    create_by = models.CharField(max_length=255, help_text='create user')
    update_by = models.CharField(max_length=255, help_text='last update user')
    suite_dir = models.ForeignKey(SuiteDir, related_name='suites', on_delete=models.CASCADE, help_text='associated dir')
    project_id = models.IntegerField(help_text='associated project')
    timeout = models.CharField(default=None, blank=True, null=True, max_length=255, help_text='all case run timeout')
    status = models.IntegerField(default=0, help_text='test suite status')

    class Meta:
        verbose_name = 'test suite'
        verbose_name_plural = verbose_name
        db_table = 'test_suite'
        unique_together = ['name', 'suite_dir']
