from django.db import models

# Create your models here.


class Department(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(max_length=255, help_text='department name')

    class Meta:
        verbose_name = 'department'
        verbose_name_plural = verbose_name
        db_table = 'department'
