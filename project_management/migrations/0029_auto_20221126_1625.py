# Generated by Django 3.2.16 on 2022-11-26 10:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0028_result_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marksheet',
            name='result',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='marksheet', to='project_management.result', verbose_name='Result'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposal', to='project_management.course', verbose_name='Course'),
        ),
    ]
