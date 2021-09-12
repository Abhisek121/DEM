# Generated by Django 3.1.7 on 2021-04-24 16:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_auto_20210424_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='time_in',
            field=models.TimeField(default=datetime.datetime(2021, 4, 24, 22, 34, 59, 143160)),
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('date', models.DateField(default=None, max_length=100)),
                ('status', models.CharField(max_length=100, null=True)),
                ('temp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.employee')),
            ],
        ),
    ]
