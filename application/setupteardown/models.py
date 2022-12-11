from django.db import models
from django.conf import settings

# Create your models here.


class SetupTeardown(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='primary key id')
    module_id = models.IntegerField(help_text='associated module id')
    module_type = models.IntegerField(default=0, choices=settings.MODULE_TYPE,
                                      help_text='associated module type')
    module_setup = models.TextField(default=None, null=True, blank=True, help_text='module setup steps')
    module_teardown = models.TextField(default=None, null=True, blank=True, help_text='module teardown step')
    module_setup_desc = models.TextField(default=None, null=True, blank=True, help_text='module setup step desc')
    module_teardown_desc = models.TextField(default=None, null=True, blank=True, help_text='module teardown step desc')
    test_setup = models.TextField(default=None, null=True, blank=True, help_text='test case setup step')
    test_teardown = models.TextField(default=None, null=True, blank=True, help_text='test case teardown step')
    test_setup_desc = models.TextField(default=None, null=True, blank=True, help_text='test case setup step desc')
    test_teardown_desc = models.TextField(default=None, null=True, blank=True, help_text='test case teardown step desc')

    class Meta:
        verbose_name = 'setup teardown'
        verbose_name_plural = verbose_name
        db_table = 'setup_teardown'
