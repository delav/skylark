from django.db import models

# Create your models here.


class PythonLib(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    lib_name = models.CharField(max_length=255, help_text='lib name')
    lib_type = models.IntegerField(default=1, choices=((1, 'builtin'), (2, 'customize')),
                                   help_text='python library type')
    lib_path = models.CharField(max_length=255, help_text='library path')
    lib_desc = models.TextField(default=None, null=True, help_text='lib description')

    class Meta:
        verbose_name = 'python lib'
        verbose_name_plural = verbose_name
        db_table = 'python_lib'
