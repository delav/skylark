from django.db import models
from application.testcase.models import TestCase
from application.libkeyword.models import LibKeyword
from application.userkeyword.models import UserKeyword

# Create your models here.


class CaseEntity(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    input_parm = models.TextField(default=None, blank=True, null=True,  help_text='input parameters')
    output_parm = models.TextField(default=None, blank=True, null=True, help_text='output parameters')
    seq_number = models.IntegerField(help_text='entity sequence number')
    test_case = models.ForeignKey(TestCase, null=True, related_name='entity', on_delete=models.CASCADE,
                                  help_text='associated case')
    keyword_id = models.IntegerField(help_text='lib keyword or user keyword id')
    keyword_type = models.IntegerField(default=1, choices=((1, 'lib_keyword'), (2, 'user_keyword')),
                                       help_text='keyword type')
    # keyword = models.ForeignKey(LibKeyword, null=True, on_delete=models.CASCADE,
    #                             help_text='associated lib keyword')
    # user_keyword = models.ForeignKey(UserKeyword, null=True, on_delete=models.CASCADE,
    #                                  help_text='associated user keyword')

    class Meta:
        verbose_name = 'case entity'
        verbose_name_plural = verbose_name
        db_table = 'case_entity'
        unique_together = ['test_case', 'seq_number']

