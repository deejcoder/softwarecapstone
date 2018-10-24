# Generated by Django 2.0.6 on 2018-10-24 11:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20181024_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 24, 11, 2, 47, 4997, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='job',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 7, 11, 2, 47, 4997, tzinfo=utc)),
        ),
    ]