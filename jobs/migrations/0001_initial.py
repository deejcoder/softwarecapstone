# Generated by Django 2.0.6 on 2018-10-24 05:16

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entity', '0002_auto_20181016_0423'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=30)),
                ('short_description', models.TextField(default='', max_length=150)),
                ('description', models.TextField(max_length=3500)),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='A phone number can only contain numbers.', regex='^[0-9]*$')])),
                ('date_posted', models.DateTimeField(default=datetime.datetime(2018, 10, 24, 5, 16, 17, 791177, tzinfo=utc))),
                ('expiry', models.DateTimeField(default=datetime.datetime(2018, 11, 7, 5, 16, 17, 791177, tzinfo=utc))),
                ('external_link', models.CharField(blank=True, default=None, max_length=2072)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='entity.Company')),
            ],
        ),
    ]
