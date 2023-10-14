from django.db import models
from application.testcase.models import TestCase
from application.project.models import Project

# Create your models here.


class UserKeyword(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    group_id = models.IntegerField(help_text='associated keyword group')
    image = models.ImageField(default='icons/keyword/user.svg', upload_to='icons/keyword', help_text='keyword icon')
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, help_text='associated test case')
    project_id = models.IntegerField(help_text='associated project')
    status = models.IntegerField(default=0, help_text='module status')

    class Meta:
        verbose_name = 'user keyword'
        verbose_name_plural = verbose_name
        db_table = 'user_keyword'
