# Generated by Django 2.0.1 on 2018-03-22 02:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0020_auto_20180322_0351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='claim',
            old_name='vallid',
            new_name='valid',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2045, 8, 6, 2, 53, 44, 420038, tzinfo=utc)),
        ),
    ]
