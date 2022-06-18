from django.db import models
from datetime import datetime
from application.project.models import Project
from application.suite_dir.models import SuiteDir

# Create your models here.


class TestSuite(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='主键')
    suite_name = models.CharField(max_length=255, help_text='套件名称')
    create_at = models.DateTimeField(verbose_name='创建时间', default=datetime.now, help_text='创建时间')
    update_at = models.DateTimeField(verbose_name='更新时间', default=datetime.now, help_text='更新时间')
    project = models.ForeignKey(Project, null=True, related_name='p_suites', on_delete=models.CASCADE, help_text='关联项目')
    suite_dir = models.ForeignKey(SuiteDir, null=True, related_name='d_suites', on_delete=models.CASCADE, help_text='关联目录')
    suite_type = models.IntegerField(default=0, choices=((0, 'robot'), (1, 'resource'), (2, 'file')), help_text='套件类型')
    deleted = models.BooleanField(default=1, help_text='是否已删除')

    class Meta:
        verbose_name = '测试套件表'
        verbose_name_plural = verbose_name
        db_table = 'test_suite'
        ordering = ['create_at']
        unique_together = ['suite_name', 'suite_dir', 'project']