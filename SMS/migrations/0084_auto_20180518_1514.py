# Generated by Django 2.0.1 on 2018-05-18 13:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0083_auto_20180517_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='due_date_D3',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 18, 15, 14, 53, 498472)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D4',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 18, 15, 14, 53, 498496)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D5',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 18, 15, 14, 53, 498513)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D6',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 18, 15, 14, 53, 498527)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D8',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 18, 15, 14, 53, 498541)),
        ),
        migrations.AlterField(
            model_name='ishikawa_detection',
            name='machine',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='ishikawa_detection',
            name='man',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='ishikawa_detection',
            name='material',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='ishikawa_detection',
            name='method',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='ishikawa_detection',
            name='problem',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='ishikawa_occurance',
            name='machine',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='ishikawa_occurance',
            name='man',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='ishikawa_occurance',
            name='material',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='ishikawa_occurance',
            name='method',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='ishikawa_occurance',
            name='problem',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
