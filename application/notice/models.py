from django.db import models


# Create your models here.

class Notice(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    project_id = models.IntegerField(help_text='associated project')
    create_at = models.DateTimeField(auto_now_add=True, help_text='build time')
    update_at = models.DateTimeField(auto_now=True, help_text='last update time')
    create_by = models.CharField(max_length=255, help_text='create user')
    update_by = models.CharField(max_length=255, help_text='last update user')
    ding_token = models.TextField(default=None, blank=True, null=True, help_text='ding talk token')
    ding_keyword = models.TextField(default=None, blank=True, null=True, help_text='ding talk keyword')
    wecom_token = models.TextField(default=None, blank=True, null=True, help_text='wecom token')
    wecom_keyword = models.TextField(default=None, blank=True, null=True, help_text='wecom keyword')
    lark_token = models.TextField(default=None, blank=True, null=True, help_text='lark token')
    lark_keyword = models.TextField(default=None, blank=True, null=True, help_text='lark keyword')
    notice_mode = models.IntegerField(default=0, help_text='notice mode')
    notice_switch = models.BooleanField(default=False,  help_text='notice switch')
    rcv_email = models.TextField(default=None, blank=True, null=True, help_text='notice email address')
    email_switch = models.BooleanField(default=False, help_text='email notify switch')

    class Meta:
        verbose_name = 'notice'
        verbose_name_plural = verbose_name
        db_table = 'notice'
