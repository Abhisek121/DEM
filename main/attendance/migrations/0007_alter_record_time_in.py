# Generated by Django 3.2.6 on 2021-09-09 08:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_alter_record_time_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='time_in',
            field=models.TimeField(default=datetime.datetime(2021, 9, 9, 13, 52, 1, 700898)),
        ),
    ]