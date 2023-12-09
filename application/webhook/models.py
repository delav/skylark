from django.db import models

# Create your models here.


def extra_data_dict():
    return {}


class Webhook(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(max_length=255, help_text='hook name')
    secret = models.CharField(max_length=255, help_text='webhook secret')
    hook_type = models.IntegerField(default=1, help_text='webhook type')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    create_by = models.CharField(max_length=255, help_text='create user')
    update_by = models.CharField(max_length=255, help_text='last update user')
    status = models.IntegerField(default=0, help_text='module status')
    desc = models.TextField(default=None, blank=True, null=True, help_text='hook desc')
    extra_data = models.JSONField(default=extra_data_dict, help_text='extra data')

    class Meta:
        verbose_name = 'webhook'
        verbose_name_plural = verbose_name
        db_table = 'webhook'
