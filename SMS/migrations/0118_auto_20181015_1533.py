# Generated by Django 2.0.6 on 2018-10-15 13:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0117_auto_20181011_0206'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='vendor_nb',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='vendor nb / customer nb'),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D3',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 15, 15, 33, 31, 47745)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D4',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 15, 15, 33, 31, 47780)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D5',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 15, 15, 33, 31, 47809)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D6',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 15, 15, 33, 31, 47832)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D8',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 15, 15, 33, 31, 47854)),
        ),
        migrations.AlterField(
            model_name='company',
            name='DUNS',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
