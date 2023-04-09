from django.db import models

# Create your models here.


class Region(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(max_length=255, help_text='region name')
    ext_name = models.CharField(default=None, max_length=255, help_text='external name')

    class Meta:
        verbose_name = 'region'
        verbose_name_plural = verbose_name
        db_table = 'region'
