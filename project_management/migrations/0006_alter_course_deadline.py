# Generated by Django 3.2.16 on 2022-11-15 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0005_alter_proposal_assigned_supervisor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='deadline',
            field=models.DateField(verbose_name='Deadline'),
        ),
    ]
