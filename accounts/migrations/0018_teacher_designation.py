# Generated by Django 3.2.16 on 2022-12-15 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='designation',
            field=models.CharField(default=1, max_length=128, verbose_name='Designation'),
            preserve_default=False,
        ),
    ]
