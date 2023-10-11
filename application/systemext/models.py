from django.db import models

# Create your models here.


class SystemExt(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    user_id = models.IntegerField(help_text='related user id')
    info_type = models.IntegerField(help_text='data type')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='end time')
    extra_data = models.TextField(default='{}', help_text='extra data')

    class Meta:
        verbose_name = 'system ext'
        verbose_name_plural = verbose_name
        db_table = 'system_ext'
