from django.db import models

# Create your models here.


class SetupTeardown(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='主键')
    module_id = models.IntegerField(help_text='关联模块ID')
    module_type = models.IntegerField(default=0, choices=((0, '项目'), (1, '目录'), (2, '套件')), help_text='关联模块类型')
    module_setup = models.TextField(default=None, null=True, blank=True, help_text='模块setup步骤')
    module_teardown = models.TextField(default=None, null=True, blank=True, help_text='模块teardown步骤')
    module_setup_desc = models.TextField(default=None, null=True, blank=True, help_text='模块setup步骤描述')
    module_teardown_desc = models.TextField(default=None, null=True, blank=True, help_text='模块teardown步骤描述')
    test_setup = models.TextField(default=None, null=True, blank=True, help_text='测试用例setup步骤')
    test_teardown = models.TextField(default=None, null=True, blank=True, help_text='测试用例teardown步骤')
    test_setup_desc = models.TextField(default=None, null=True, blank=True, help_text='测试用例setup步骤描述')
    test_teardown_desc = models.TextField(default=None, null=True, blank=True, help_text='测试用例teardown步骤描述')

    class Meta:
        verbose_name = '前置后置表'
        verbose_name_plural = verbose_name
        db_table = 'setup_teardown'
