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
    group = models.ForeignKey(KeywordGroup, on_delete=models.CASCADE, help_text='associated group')
    image = models.ImageField(default='icons/keyword/user.svg', upload_to='icons/keyword', help_text='keyword icon')
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, help_text='associated test case')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, help_text='associated project')

    class Meta:
        verbose_name = 'user keyword'
        verbose_name_plural = verbose_name
        db_table = 'user_keyword'
