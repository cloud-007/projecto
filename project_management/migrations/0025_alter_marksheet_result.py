# Generated by Django 3.2.16 on 2022-11-26 05:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0024_alter_marksheet_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marksheet',
            name='result',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='marksheets', to='project_management.result', verbose_name='Result'),
        ),
    ]
