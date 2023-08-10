from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(max_length=255, help_text='product name')
    department_id = models.IntegerField(help_text='associated department')

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = verbose_name
        db_table = 'product'
