# Generated by Django 2.0.6 on 2018-11-01 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verify_code',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]