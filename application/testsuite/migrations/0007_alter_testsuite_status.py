# Generated by Django 3.2.13 on 2023-10-16 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsuite', '0006_alter_testsuite_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testsuite',
            name='status',
            field=models.IntegerField(default=0, help_text='module status'),
        ),
    ]
