from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


User = get_user_model()

# class Role(models.Model):
#     id = models.BigAutoField(primary_key=True, help_text='primary key id')
#     name = models.CharField(max_length=255, help_text='role name')
#
#
# class User(AbstractUser):
#     role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, help_text='role')
