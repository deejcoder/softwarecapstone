# Generated by Django 2.0.6 on 2018-10-24 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0005_auto_20181024_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='introduction',
            field=models.TextField(default='Nothing', max_length=300),
            preserve_default=False,
        ),
    ]