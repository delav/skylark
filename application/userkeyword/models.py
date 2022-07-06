from django.db import models
from datetime import datetime
from application.keywordgroup.models import KeywordGroup
from application.testcase.models import TestCase
from application.project.models import Project

# Create your models here.


class UserKeyword(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='主键')
    create_at = models.DateTimeField(verbose_name='创建时间', default=datetime.now, help_text='创建时间')
    update_at = models.DateTimeField(verbose_name='更新时间', default=datetime.now, help_text='更新时间')
    group = models.ForeignKey(KeywordGroup, null=True, on_delete=models.CASCADE, help_text='所属分组')
    image = models.ImageField(default='media/%Y/%m/%d/', blank=True, null=True, help_text='展示图标')
    test_case = models.ForeignKey(TestCase, null=True, on_delete=models.CASCADE, related_name='tcs', help_text='关联用例')
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE, related_name='uks', help_text='关联项目')

    class Meta:
        verbose_name = '用户关键字表'
        verbose_name_plural = verbose_name
        db_table = 'user_keyword'
