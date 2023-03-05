from django.db import models

# Create your models here.


class CasePriority(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary kwy id')
    name = models.CharField(max_length=255, help_text='priority name')

    class Meta:
        verbose_name = 'case priority'
        verbose_name_plural = verbose_name
        db_table = 'case_priority'
