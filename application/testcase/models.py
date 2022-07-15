from django.db import models
from datetime import datetime
from application.testsuite.models import TestSuite
from application.casetag.models import CaseTag

# Create your models here.


class TestCase(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='主键')
    case_name = models.CharField(max_length=255, help_text='用例名称')
    case_desc = models.TextField(default=None, blank=True, null=True, help_text='用例描述')
    create_at = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_at = models.DateTimeField(auto_now=True, help_text='更新时间')
    case_pri = models.IntegerField(default=3, choices=((0, 'P0'), (1, 'P1'), (2, 'P2'), (3, 'P3')), help_text='用例优先级')
    case_tag = models.ManyToManyField(CaseTag, related_name='tags', default='', blank=True, help_text='用例标签')
    test_suite = models.ForeignKey(TestSuite, related_name='cases', null=True, on_delete=models.CASCADE, help_text='关联测试套件')
    case_type = models.IntegerField(default=0, choices=((0, 'T0'), (1, 'T1')), help_text='用例类型, 0: 普通用例; 1:用户关键字')
    inputs = models.TextField(default=None, blank=True, null=True, help_text='输入参数')
    outputs = models.TextField(default=None, blank=True, null=True, help_text='输出参数')
    deleted = models.BooleanField(default=1, help_text='是否已删除')

    class Meta:
        verbose_name = '测试用例表'
        verbose_name_plural = verbose_name
        db_table = 'test_case'
        ordering = ['create_at']
        unique_together = ['case_name', 'test_suite']