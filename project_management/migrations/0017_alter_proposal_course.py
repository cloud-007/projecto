# Generated by Django 3.2.16 on 2022-11-23 12:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0016_alter_marksheet_proposal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposal', to='project_management.course', verbose_name='Course'),
        ),
    ]