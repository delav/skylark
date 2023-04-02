from django.db import models
from application.user.models import User

# Create your models here.


class Project(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    name = models.CharField(unique=True, max_length=255, help_text='project name')
    create_at = models.DateTimeField(auto_now_add=True,  help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='update time')
    create_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,
                                  related_name='pro_cuser', help_text='create user')
    update_by = models.ForeignKey(User, blank=True, null=True, related_name='pro_muser',
                                  on_delete=models.DO_NOTHING, help_text='last update user')
    deleted = models.BooleanField(default=0, help_text='if deleted')

    class Meta:
        verbose_name = 'project'
        verbose_name_plural = verbose_name
        db_table = 'project'
        ordering = ['create_at']