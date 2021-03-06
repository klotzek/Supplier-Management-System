# Generated by Django 2.0.1 on 2018-06-04 06:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0096_auto_20180529_1445'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='group',
            new_name='action',
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D3',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 4, 8, 40, 0, 488192)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D4',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 4, 8, 40, 0, 488219)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D5',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 4, 8, 40, 0, 488236)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D6',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 4, 8, 40, 0, 488250)),
        ),
        migrations.AlterField(
            model_name='claim',
            name='due_date_D8',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 4, 8, 40, 0, 488264)),
        ),
    ]
