from django.db import models

# Create your models here.


class Region(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(max_length=255, help_text='region name')
    desc = models.CharField(default='', max_length=255, help_text='region desc')
    status = models.IntegerField(default=0, help_text='region status')

    class Meta:
        verbose_name = 'region'
        verbose_name_plural = verbose_name
        db_table = 'region'
