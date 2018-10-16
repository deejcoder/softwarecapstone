# Generated by Django 2.0.6 on 2018-10-15 23:55

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
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 15, 23, 55, 0, 535106, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='job',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 29, 23, 55, 0, 535106, tzinfo=utc)),
        ),
    ]