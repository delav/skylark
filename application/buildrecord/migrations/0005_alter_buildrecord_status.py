# Generated by Django 3.2.13 on 2023-10-16 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildrecord', '0004_buildrecord_finish_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildrecord',
            name='status',
            field=models.IntegerField(default=0, help_text='build status'),
        ),
    ]
