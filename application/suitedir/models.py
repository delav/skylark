from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
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
    dir_type = models.IntegerField(default=0, choices=settings.MODEL_TYPE, help_text='dir type')
    deleted = models.BooleanField(default=1, help_text='if deleted')

    class Meta:
        verbose_name = 'suite dir'
        verbose_name_plural = verbose_name
        db_table = 'suite_dir'
        ordering = ['dir_name']
        unique_together = [('project', 'parent_dir', 'dir_name')]

    def clean(self):
        """
        Checks that we do not create multiple suite dir with
        no parent dir and the same project and dir name.
        """
        if self.parent_dir is None and SuiteDir.objects.filter(
                project_id=self.project_id,
                parent_dir_id=self.parent_dir_id,
                dir_name=self.dir_name).exists():
            raise ValidationError("Another Dir with name=%s and no parent already exists" % self.dir_name)

    def save(self, *args, **kwargs):
        self.clean()
        return super(SuiteDir, self).save(*args, **kwargs)