# Generated by Django 2.0.1 on 2018-04-13 14:38

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0029_auto_20180403_2140'),
    ]

    operations = [
        migrations.CreateModel(
            name='D1D3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('refuse', models.BooleanField(default=False)),
                ('production_date', models.DateTimeField()),
                ('claim', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SMS.Claim')),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2045, 8, 28, 14, 38, 45, 813899, tzinfo=utc)),
        ),
    ]
