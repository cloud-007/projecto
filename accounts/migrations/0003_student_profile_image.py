# Generated by Django 3.2.16 on 2022-11-17 05:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_student_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile_image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='', verbose_name='Profile'),
            preserve_default=False,
        ),
    ]