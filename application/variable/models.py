from django.db import models

# Create your models here.


class Variable(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='主键')
    module_id = models.IntegerField(help_text='关联模块ID')
    module_type = models.IntegerField(default=0, choices=((0, '项目'), (1, '目录'), (2, '套件')), help_text='关联模块类型')
    name = models.CharField(max_length=255, help_text='变量名称')
    value = models.TextField(null=True, blank=True, help_text='变量值')
    value_type = models.IntegerField(default=0, choices=((0, '字符'), (1, '列表'), (2, '字典')), help_text='变量值类型')
    env = models.IntegerField(default=1, choices=((0, 'DEV'), (1, 'TEST'), (2, 'UAT'), (3, 'STAGING')), help_text='环境')
    remark = models.TextField(null=True, blank=True, help_text='备注')

    class Meta:
        verbose_name = '变量表'
        verbose_name_plural = verbose_name
        db_table = 'variable'
