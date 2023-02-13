# Generated by Django 3.2.16 on 2023-02-07 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0032_course_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(choices=[('CSE_3300', 'CSE 3300'), ('CSE_4800', 'CSE 4800'), ('CSE_4801', 'CSE 4801')], default='CSE_3300', max_length=32, verbose_name='Title'),
        ),
    ]