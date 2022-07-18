from django.db import models
from application.project.models import Project

# Create your models here.


class SuiteDir(models.Model):

    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    dir_name = models.CharField(max_length=255, help_text='dir name')
    create_at = models.DateTimeField(auto_now_add=True, help_text='create time')
    update_at = models.DateTimeField(auto_now=True, help_text='end time')
    project = models.ForeignKey(Project, null=True, related_name='dirs', on_delete=models.CASCADE,
                                help_text='associated project')
    parent_dir = models.ForeignKey('self', related_name='children', null=True, on_delete=models.CASCADE,
                                   help_text='parent dir')
    dir_type = models.IntegerField(default=0, choices=((0, 'robot'), (1, 'resource'), (2, 'file')),
                                   help_text='dir type')
    deleted = models.BooleanField(default=1, help_text='if deleted')

    class Meta:
        verbose_name = 'suite dir'
        verbose_name_plural = verbose_name
        db_table = 'suite_dir'
        ordering = ['create_at']
        unique_together = [('project', 'parent_dir', 'dir_name')]