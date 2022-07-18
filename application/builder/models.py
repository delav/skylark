import uuid
from django.db import models
from application.user.models import User
from application.project.models import Project

# Create your models here.


class Builder(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    nonce = models.UUIDField(default=uuid.uuid1, unique=True, help_text='nonce uuid')
    total_number = models.IntegerField(default=0, blank=True, help_text='total cases number')
    failed_number = models.IntegerField(default=0, blank=True, help_text='failure cases number')
    success_number = models.IntegerField(default=0, blank=True, help_text='successful cases number')
    start_time = models.DateTimeField(auto_now_add=True, help_text='build start time')
    end_time = models.DateTimeField(default=None, blank=True, null=True, help_text='build end time')
    build_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, help_text='build user')
    status = models.IntegerField(default=-1, blank=True,
                                 help_text='build status,-1:waiting,1:running,0:normal,9:interrupt')
    cron_job = models.BooleanField(default=False, help_text='if timing task')
    project = models.ForeignKey(Project, help_text='associated project', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'builder'
        verbose_name_plural = verbose_name
        db_table = 'builder'
