# Generated by Django 3.1.5 on 2021-01-29 16:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_auto_20210127_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='valid_from',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 29, 16, 30, 46, 904544, tzinfo=utc)),
            preserve_default=False,
        ),
    ]