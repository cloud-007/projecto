# Generated by Django 3.2.16 on 2023-02-07 16:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0030_auto_20230207_2220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='deadline',
        ),
        migrations.AddField(
            model_name='course',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='End Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Start Time'),
            preserve_default=False,
        ),
    ]
