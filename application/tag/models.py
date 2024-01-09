from django.db import models

# Create your models here.


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(max_length=255, help_text='tag name')
    project_id = models.IntegerField(help_text='associated project')

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = verbose_name
        db_table = 'tag'


class ModuleTag(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    tag_id = models.IntegerField(help_text='associated tag id')
    module_id = models.IntegerField(help_text='associated module id')
    module_type = models.IntegerField(default=0, help_text='associated module type')

    class Meta:
        verbose_name = 'module tag'
        verbose_name_plural = verbose_name
        db_table = 'module_tag'
