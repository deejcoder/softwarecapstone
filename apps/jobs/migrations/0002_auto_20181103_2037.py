# Generated by Django 2.0.6 on 2018-11-03 07:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 3, 7, 37, 15, 648243, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='job',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 17, 7, 37, 15, 648243, tzinfo=utc)),
        ),
    ]
