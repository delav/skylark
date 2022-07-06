from django.db import models
from application.testcase.models import TestCase
from application.libkeyword.models import LibKeyword
from application.userkeyword.models import UserKeyword

# Create your models here.


class CaseEntity(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='主键')
    input_parm = models.TextField(default=None, blank=True, null=True,  help_text='输入参数')
    output_parm = models.TextField(default=None, blank=True, null=True, help_text='输出参数')
    seq_number = models.IntegerField(help_text='序号')
    test_case = models.ForeignKey(TestCase, null=True, related_name='entity', on_delete=models.CASCADE, help_text='关联用例')
    keyword = models.ForeignKey(LibKeyword, null=True, on_delete=models.CASCADE, help_text='关联关键字')
    user_keyword = models.ForeignKey(UserKeyword, null=True, on_delete=models.CASCADE, help_text='关联用户关键字')

    class Meta:
        verbose_name = '用例实体表'
        verbose_name_plural = verbose_name
        db_table = 'case_entity'
        unique_together = ['test_case', 'seq_number']

