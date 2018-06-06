# Generated by Django 2.0.1 on 2018-05-17 11:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0081_auto_20180509_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ishikawa_detection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=250)),
                ('machine', models.CharField(max_length=250)),
                ('man', models.CharField(max_length=250)),
                ('material', models.CharField(max_length=250)),
                ('problem', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Ishikawa_occurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=250)),
                ('machine', models.CharField(max_length=250)),
                ('man', models.CharField(max_length=250)),
                ('material', models.CharField(max_length=250)),
                ('problem', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D3',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 17, 13, 11, 20, 210458)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D4',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 17, 13, 11, 20, 210484)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D5',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 17, 13, 11, 20, 210501)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D6',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 17, 13, 11, 20, 210516)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D8',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 17, 13, 11, 20, 210532)),
        ),
        migrations.AddField(
            model_name='ishikawa_occurance',
            name='claim',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SMS.Claim'),
        ),
        migrations.AddField(
            model_name='ishikawa_detection',
            name='claim',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SMS.Claim'),
        ),
    ]
