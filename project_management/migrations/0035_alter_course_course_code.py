# Generated by Django 3.2.16 on 2023-02-07 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0034_auto_20230207_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_code',
            field=models.CharField(choices=[('3300', 'CSE 3300'), ('4800', 'CSE 4800'), ('4801', 'CSE 4801')], default='3300', max_length=32, verbose_name='Title'),
        ),
    ]