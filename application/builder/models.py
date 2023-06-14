from django.db import models
from application.project.models import Project
from application.environment.models import Environment

# Create your models here.


class Builder(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    create_at = models.DateTimeField(auto_now_add=True, help_text='build time')
    create_by = models.CharField(max_length=255, help_text='create user')

    class Meta:
        verbose_name = 'builder'
        verbose_name_plural = verbose_name
        db_table = 'builder'
