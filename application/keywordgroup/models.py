from django.db import models

# Create your models here.


class KeywordGroup(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(unique=True, max_length=255, help_text='keyword group name')
    image = models.ImageField(default='media/icons/group/default.png', blank=True, null=True, help_text='icon')
    group_type = models.IntegerField(default=0, help_text='keyword group type, 0: lib, 1: user')
    project_id = models.IntegerField(default=None, null=True, help_text='associated project')
    
    class Meta:
        verbose_name = 'keyword group'
        verbose_name_plural = verbose_name
        db_table = 'keyword_group'
