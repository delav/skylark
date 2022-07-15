import uuid
from django.db import models
from application.user.models import User
from application.project.models import Project

# Create your models here.


class Builder(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='主键')
    nonce = models.UUIDField(default=uuid.uuid1, unique=True, help_text='随机字符串')
    total_number = models.IntegerField(default=0, blank=True, help_text='用例总数')
    failed_number = models.IntegerField(default=0, blank=True, help_text='失败用例数')
    success_number = models.IntegerField(default=0, blank=True, help_text='成功用例数')
    start_time = models.DateTimeField(auto_now_add=True, help_text='开始时间')
    end_time = models.DateTimeField(default=None, blank=True, null=True, help_text='结束时间')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, help_text='构建用户')
    status = models.IntegerField(default=-1, blank=True, help_text='执行状态,-1:放入队列,1:正在执行,0:正常结束,9:异常终止')
    fixed_task = models.BooleanField(default=False, help_text='是否为定时任务')
    project = models.ForeignKey(Project, help_text='所属项目', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '构建表'
        verbose_name_plural = verbose_name
        db_table = 'builder'
