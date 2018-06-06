# Generated by Django 2.0.1 on 2018-04-14 23:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0039_auto_20180414_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='production_date_1',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2045, 8, 29, 23, 0, 25, 887924, tzinfo=utc)),
        ),
    ]
