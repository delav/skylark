from django.db import models

# Create your models here.


def extra_data_dict():
    return {}


class WorkerManager(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    ip = models.CharField(max_length=255, help_text='worker ip addr')
    hostname = models.CharField(max_length=255, help_text='worker host name')
    alive = models.BooleanField(default=True, help_text='worker state')
    queue = models.CharField(max_length=255, help_text='worker exclusive queue')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    extra_data = models.JSONField(default=extra_data_dict, help_text='extra data')

    class Meta:
        verbose_name = 'worker manager'
        verbose_name_plural = verbose_name
        db_table = 'worker_manager'
