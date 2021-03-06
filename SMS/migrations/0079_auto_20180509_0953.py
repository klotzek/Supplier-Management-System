# Generated by Django 2.0.1 on 2018-05-09 07:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0078_auto_20180509_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='penalty_periods',
            name='penaltyModel',
            field=models.CharField(default='Standard', max_length=25),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D3',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 9, 9, 53, 10, 729767)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D4',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 9, 9, 53, 10, 729791)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D5',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 9, 9, 53, 10, 729807)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D6',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 9, 9, 53, 10, 729822)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D8',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 9, 9, 53, 10, 729836)),
        ),
    ]
