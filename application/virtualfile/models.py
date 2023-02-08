from django.db import models
from application.testsuite.models import TestSuite

# Create your models here.


class VirtualFile(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    file_subfix = models.CharField(max_length=255, help_text='file subfix name')
    file_text = models.TextField(null=True, blank=True, help_text='py file content')
    test_suite = models.ForeignKey(TestSuite, null=True, related_name='suite', on_delete=models.CASCADE,
                                   help_text='associated suite')
    remark = models.TextField(null=True, blank=True, help_text='remark')

    class Meta:
        verbose_name = 'virtual file'
        verbose_name_plural = verbose_name
        db_table = 'virtual_file'
