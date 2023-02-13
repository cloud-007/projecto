# Generated by Django 3.2.16 on 2023-02-13 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0037_auto_20230213_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(choices=[('CSE 3300', 'Project I'), ('CSE 4800', 'Project II part I'), ('CSE 4801', 'Project II part II')], default='Project I', max_length=32, verbose_name='Title'),
        ),
    ]
