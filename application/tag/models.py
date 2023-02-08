from django.db import models
from django.conf import settings

# Create your models here.


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(max_length=255, help_text='tag name')
    module_id = models.IntegerField(help_text='associated module id')
    module_type = models.IntegerField(default=0, choices=settings.MODULE_TYPE, help_text='associated module type')

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = verbose_name
        db_table = 'tag'
