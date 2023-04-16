# Generated by Django 3.2.16 on 2023-02-18 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0043_remove_notice_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='state',
            field=models.CharField(choices=[('RUNNING', 'Running'), ('ARCHIVED', 'Archived'), ('UPCOMING', 'Upcoming'), ('DELETED', 'Deleted')], default='RUNNING', max_length=32, verbose_name='State'),
        ),
    ]