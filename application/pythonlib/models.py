from django.db import models

# Create your models here.


class PythonLib(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    lib_name = models.CharField(max_length=255, help_text='lib name')
    lib_type = models.IntegerField(default=1, help_text='python library type')
    lib_path = models.CharField(max_length=255, help_text='library path')
    lib_desc = models.TextField(default=None, blank=True, null=True, help_text='lib description')
    user_group_id = models.IntegerField(default=None, null=True, blank=True, help_text='related user group')

    class Meta:
        verbose_name = 'python lib'
        verbose_name_plural = verbose_name
        db_table = 'python_lib'
