# Generated by Django 3.2.16 on 2022-11-20 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_remove_student_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='email',
            field=models.CharField(default=12345, max_length=56, verbose_name='Email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='phone',
            field=models.IntegerField(default=12345, verbose_name='Phone'),
            preserve_default=False,
        ),
    ]