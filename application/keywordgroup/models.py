from django.db import models

# Create your models here.


class KeywordGroup(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    group_name = models.CharField(unique=True, max_length=255, help_text='keyword group name')
    
    class Meta:
        verbose_name = 'keyword group'
        verbose_name_plural = verbose_name
        db_table = 'keyword_group'
