# Generated by Django 3.2.16 on 2022-11-20 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_student_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='profile_image',
        ),
    ]
