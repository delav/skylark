from django.db import models
from application.builder.models import Builder

# Create your models here.


class BuildCase(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='主键')
    suite_name = models.CharField(max_length=255, help_text='测试套件名称')
    case_id = models.IntegerField(help_text='用例ID')
    case_name = models.CharField(max_length=255, help_text='用例名称')
    start_time = models.DateTimeField(null=True, blank=True, help_text='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, help_text='执行时间')
    status = models.IntegerField(default=-1, help_text='执行结果.-1:未执行,0:失败,1:成功')
    builder = models.ForeignKey(Builder, on_delete=models.CASCADE, help_text='构建编号')

    class Meta:
        verbose_name = '构建用例表'
        verbose_name_plural = verbose_name
        db_table = 'buidl_case'
