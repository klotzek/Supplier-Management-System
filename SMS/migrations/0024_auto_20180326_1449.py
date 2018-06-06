# Generated by Django 2.0.1 on 2018-03-26 12:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0023_auto_20180326_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='due_date',
            field=models.DateTimeField(default=0.0004761904761904762),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2045, 8, 10, 12, 49, 46, 813962, tzinfo=utc)),
        ),
    ]
