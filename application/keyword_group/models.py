from django.db import models

# Create your models here.


class KeywordGroup(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='主键')
    group_name = models.CharField(unique=True, max_length=255, help_text='分组名称')
    
    class Meta:
        verbose_name = '关键字分组表'
        verbose_name_plural = verbose_name
        db_table = 'keyword_group'
