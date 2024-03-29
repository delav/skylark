from django.db import models
from django.conf import settings

# Create your models here.
DEFAULT_ICON = settings.KEYWORD_ICON_PATH + 'default.png'


class LibKeyword(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(max_length=255, unique=True, help_text='keyword name')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    create_by = models.CharField(max_length=255, help_text='create user')
    update_by = models.CharField(max_length=255, help_text='last update user')
    ext_name = models.CharField(max_length=255, unique=True, help_text='external name')
    desc = models.TextField(default=None, blank=True, null=True, help_text='keyword desc')
    group_id = models.IntegerField(help_text='associated keyword group')
    input_params = models.TextField(default=None, blank=True, null=True, help_text='input params')
    input_desc = models.TextField(default=None, blank=True, null=True, help_text='input params desc')
    output_params = models.TextField(default=None, blank=True, null=True, help_text='output params')
    output_desc = models.TextField(default=None, blank=True, null=True, help_text='output params desc')
    input_type = models.IntegerField(default=0, help_text='input arg type')
    output_type = models.IntegerField(default=0, help_text='output  arg type')
    category = models.IntegerField(default=1, help_text='keyword category')
    image = models.ImageField(default=DEFAULT_ICON, upload_to=settings.KEYWORD_ICON_PATH, help_text='keyword icon')
    status = models.IntegerField(default=0, help_text='module status')
    library_id = models.IntegerField(default=0, help_text='related python library')
    remark = models.TextField(default=None, blank=True, null=True, help_text='keyword other remark')

    class Meta:
        verbose_name = 'lib keyword'
        verbose_name_plural = verbose_name
        db_table = 'lib_keyword'
