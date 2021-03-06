# Generated by Django 2.0.1 on 2018-05-04 06:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0055_auto_20180503_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='d3',
            name='FC_necessary',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
        migrations.AddField(
            model_name='d3',
            name='action_1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='d3',
            name='action_2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='d3',
            name='action_3',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='d3',
            name='date_1',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='d3',
            name='date_2',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='d3',
            name='date_3',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='d3',
            name='pilot_1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='d3',
            name='pilot_2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='d3',
            name='pilot_3',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D4',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 4, 8, 46, 38, 296418)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D5',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 4, 8, 46, 38, 296442)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D6',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 4, 8, 46, 38, 296459)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D8',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 4, 8, 46, 38, 296475)),
        ),
    ]
