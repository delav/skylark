from django.db import models
from django.conf import settings
from application.project.models import Project
from application.suitedir.models import SuiteDir
from application.tag.models import Tag

# Create your models here.


class TestSuite(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(max_length=255, help_text='test suite name')
    document = models.TextField(default=None, blank=True, null=True, help_text='suite desc')
    category = models.IntegerField(default=0, choices=settings.CATEGORY, help_text='model category')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    tags = models.ManyToManyField(Tag, related_name='stags', blank=True, help_text='suite tags')
    suite_dir = models.ForeignKey(SuiteDir, null=True, related_name='suites', on_delete=models.CASCADE,
                                  help_text='associated dir')
    timeout = models.CharField(default=None, null=True, max_length=255, help_text='all case run timeout')
    deleted = models.BooleanField(default=0, help_text='if deleted')

    class Meta:
        verbose_name = 'test suite'
        verbose_name_plural = verbose_name
        db_table = 'test_suite'
        ordering = ['name']
        unique_together = ['name', 'suite_dir']