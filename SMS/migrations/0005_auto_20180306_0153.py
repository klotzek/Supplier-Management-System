# Generated by Django 2.0.1 on 2018-03-06 00:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0004_auto_20180306_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2045, 7, 21, 0, 53, 42, 636380, tzinfo=utc)),
        ),
    ]
