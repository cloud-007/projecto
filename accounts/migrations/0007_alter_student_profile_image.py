# Generated by Django 3.2.16 on 2022-11-17 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_student_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profile_image',
            field=models.ImageField(default='profile/defaultProfile.png', upload_to='profile/', verbose_name='Profile'),
        ),
    ]