from django.db import models
from application.project.models import Project

# Create your models here.


class SuiteDir(models.Model):

    id = models.BigAutoField(primary_key=True, help_text='主键')
    dir_name = models.CharField(max_length=255, help_text='目录名称')
    create_at = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_at = models.DateTimeField(auto_now=True, help_text='更新时间')
    project = models.ForeignKey(Project, null=True, related_name='dirs', on_delete=models.CASCADE, help_text='所属项目')
    parent_dir = models.ForeignKey('self', related_name='children', null=True, on_delete=models.CASCADE, help_text='父级目录')
    dir_type = models.IntegerField(default=0, choices=((0, 'robot'), (1, 'resource'), (2, 'file')), help_text='目录类型')
    deleted = models.BooleanField(default=1, help_text='是否已删除')

    class Meta:
        verbose_name = '套件目录表'
        verbose_name_plural = verbose_name
        db_table = 'suite_dir'
        ordering = ['create_at']
        unique_together = [('project', 'parent_dir', 'dir_name')]