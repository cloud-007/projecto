# Generated by Django 3.2.16 on 2022-11-13 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0002_auto_20221108_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_id',
            field=models.IntegerField(max_length=16, verbose_name='Course ID'),
        ),
        migrations.AlterField(
            model_name='marksheet',
            name='criteria_1',
            field=models.CharField(max_length=128, verbose_name='Criteria 1 Mark'),
        ),
    ]