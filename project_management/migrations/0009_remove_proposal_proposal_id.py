# Generated by Django 3.2.16 on 2022-11-15 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0008_alter_course_deadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='proposal_id',
        ),
    ]