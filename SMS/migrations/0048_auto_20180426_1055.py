# Generated by Django 2.0.1 on 2018-04-26 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0047_remove_userprofile_key_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='due_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
