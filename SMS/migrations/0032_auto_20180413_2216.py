# Generated by Django 2.0.1 on 2018-04-13 20:16

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0031_auto_20180413_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teammember_1', models.CharField(blank=True, max_length=25, null=True)),
                ('function_1', models.CharField(blank=True, max_length=25, null=True)),
                ('mail_1', models.EmailField(blank=True, max_length=25, null=True)),
                ('teammember_2', models.CharField(blank=True, max_length=25, null=True)),
                ('function_2', models.CharField(blank=True, max_length=25, null=True)),
                ('mail_2', models.EmailField(blank=True, max_length=25, null=True)),
                ('teammember_3', models.CharField(blank=True, max_length=25, null=True)),
                ('function_3', models.CharField(blank=True, max_length=25, null=True)),
                ('mail_3', models.EmailField(blank=True, max_length=25, null=True)),
                ('claim', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SMS.Claim')),
            ],
        ),
        migrations.AddField(
            model_name='d1d3',
            name='pilot',
            field=models.CharField(default='pilot', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2045, 8, 28, 20, 15, 58, 87107, tzinfo=utc)),
        ),
    ]
