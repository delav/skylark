from django.db import models

# Create your models here.


class CaseTag(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    tag_name = models.CharField(max_length=255, help_text='tag name')
    project_id = models.IntegerField(default=None, null=True, help_text='associated project')

    class Meta:
        verbose_name = 'case tag'
        verbose_name_plural = verbose_name
        db_table = 'case_tag'
