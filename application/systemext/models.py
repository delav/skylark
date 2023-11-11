from django.db import models

# Create your models here.


def extra_data_dict():
    return {}


class SystemExt(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    user_id = models.IntegerField(default=None, null=True, help_text='related user')
    info_type = models.IntegerField(default=1, help_text='data type')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='end time')
    expire_at = models.DateTimeField(default=None, null=True, help_text='expire time')
    extra_data = models.JSONField(default=extra_data_dict, help_text='extra data')

    class Meta:
        verbose_name = 'system ext'
        verbose_name_plural = verbose_name
        db_table = 'system_ext'
