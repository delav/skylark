from django.db import models
from datetime import datetime
from application.user.models import User

# Create your models here.


class Project(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='主键')
    project_name = models.CharField(unique=True, max_length=255, help_text='项目名称')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='user', help_text='创建用户')

    class Meta:
        verbose_name = '项目表'
        verbose_name_plural = verbose_name
        db_table = 'project'
        ordering = ['create_at']