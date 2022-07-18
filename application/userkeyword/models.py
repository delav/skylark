from django.db import models
from datetime import datetime
from application.keywordgroup.models import KeywordGroup
from application.testcase.models import TestCase
from application.project.models import Project

# Create your models here.


class UserKeyword(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    create_at = models.DateTimeField(default=datetime.now, help_text='create time')
    update_at = models.DateTimeField(default=datetime.now, help_text='update time')
    group = models.ForeignKey(KeywordGroup, null=True, on_delete=models.CASCADE, help_text='associated group')
    image = models.ImageField(default='media/%Y/%m/%d/', blank=True, null=True, help_text='icon')
    test_case = models.ForeignKey(TestCase, null=True, on_delete=models.CASCADE, related_name='tcs',
                                  help_text='associated test case')
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE, related_name='uks',
                                help_text='associated project')

    class Meta:
        verbose_name = 'user keyword'
        verbose_name_plural = verbose_name
        db_table = 'user_keyword'
