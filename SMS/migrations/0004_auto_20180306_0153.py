# Generated by Django 2.0.1 on 2018-03-06 00:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0003_auto_20180306_0149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Vendor name'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2045, 7, 21, 0, 53, 39, 719881, tzinfo=utc)),
        ),
    ]
