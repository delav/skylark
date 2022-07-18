from django.db import models
from application.project.models import Project
from application.suitedir.models import SuiteDir

# Create your models here.


class TestSuite(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    suite_name = models.CharField(max_length=255, help_text='test suite name')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    suite_dir = models.ForeignKey(SuiteDir, null=True, related_name='suites', on_delete=models.CASCADE,
                                  help_text='associated dir')
    suite_type = models.IntegerField(default=0, choices=((0, 'robot'), (1, 'resource'), (2, 'file')),
                                     help_text='test suite type')
    timeout = models.CharField(default=None, max_length=255, help_text='all case run timeout')
    deleted = models.BooleanField(default=1, help_text='if deleted')

    class Meta:
        verbose_name = 'test suite'
        verbose_name_plural = verbose_name
        db_table = 'test_suite'
        ordering = ['create_at']
        unique_together = ['suite_name', 'suite_dir']