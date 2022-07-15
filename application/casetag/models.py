from django.db import models

# Create your models here.


class CaseTag(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='主键')
    tag_name = models.CharField(max_length=255, help_text='标签名称')
    project_id = models.IntegerField(default=None, null=True, help_text='所属项目')

    class Meta:
        verbose_name = '用例标签表'
        verbose_name_plural = verbose_name
        db_table = 'case_tag'
