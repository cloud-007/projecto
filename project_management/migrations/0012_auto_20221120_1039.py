# Generated by Django 3.2.16 on 2022-11-20 04:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0011_alter_proposal_assigned_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='marksheet',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='proposal',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='course',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='marksheet',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='marksheet',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposal',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='result',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
