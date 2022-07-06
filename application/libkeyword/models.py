from django.db import models
from application.keywordgroup.models import KeywordGroup

# Create your models here.


class LibKeyword(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='主键')
    name = models.CharField(max_length=255, unique=True, help_text='关键字名称')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')
    ext_name = models.CharField(default=None, max_length=255, help_text='对外名称')
    desc = models.TextField(default=None, blank=True, null=True, help_text='关键字描述')
    group = models.ForeignKey(KeywordGroup, null=True, on_delete=models.CASCADE, help_text='所属分组')
    input_arg = models.TextField(default=None, blank=True, null=True, help_text='输入参数')
    input_desc = models.TextField(default=None, blank=True, null=True, help_text='输入参数说明')
    out_arg = models.TextField(default=None, blank=True, null=True, help_text='输出参数')
    out_desc = models.TextField(default=None, blank=True, null=True, help_text='输出参数说明')
    image = models.ImageField(upload_to='media/%Y/%m/%d/', blank=True, null=True, help_text='展示图标')

    class Meta:
        verbose_name = '基础关键字表'
        verbose_name_plural = verbose_name
        db_table = 'lib_keyword'
