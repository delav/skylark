from django.db import models
from django.contrib.auth.models import Group

# Create your models here.


class UserGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    department_id = models.IntegerField(help_text='belong to department')

    class Meta:
        verbose_name = 'user group'
        verbose_name_plural = verbose_name
        db_table = 'user_group'
