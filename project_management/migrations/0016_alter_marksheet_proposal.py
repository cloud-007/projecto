# Generated by Django 3.2.16 on 2022-11-23 12:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0015_auto_20221123_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marksheet',
            name='proposal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marksheets', to='project_management.proposal', verbose_name='Proposals'),
        ),
    ]
