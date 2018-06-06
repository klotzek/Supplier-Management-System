# Generated by Django 2.0.1 on 2018-04-14 08:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0034_auto_20180413_2241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='d1d3',
            name='function',
        ),
        migrations.RemoveField(
            model_name='d1d3',
            name='mail',
        ),
        migrations.RemoveField(
            model_name='d1d3',
            name='pilot',
        ),
        migrations.AddField(
            model_name='team',
            name='function',
            field=models.CharField(default='function', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='mail',
            field=models.EmailField(default='mail', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='pilot',
            field=models.CharField(default='pilot', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2045, 8, 29, 8, 15, 35, 39808, tzinfo=utc)),
        ),
    ]
