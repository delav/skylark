from django.db import models
from application.keywordgroup.models import KeywordGroup

# Create your models here.


class LibKeyword(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(max_length=255, unique=True, help_text='keyword name')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    ext_name = models.CharField(default=None, max_length=255, help_text='external name')
    desc = models.TextField(default=None, blank=True, null=True, help_text='keyword desc')
    group = models.ForeignKey(KeywordGroup, null=True, on_delete=models.CASCADE, help_text='associated group')
    input_arg = models.TextField(default=None, blank=True, null=True, help_text='input args')
    input_desc = models.TextField(default=None, blank=True, null=True, help_text='input args desc')
    output_arg = models.TextField(default=None, blank=True, null=True, help_text='output args')
    output_desc = models.TextField(default=None, blank=True, null=True, help_text='output args desc')
    image = models.ImageField(upload_to='media/icons/keyword', blank=True, null=True, help_text='keyword icon')

    class Meta:
        verbose_name = 'lib keyword'
        verbose_name_plural = verbose_name
        db_table = 'lib_keyword'
