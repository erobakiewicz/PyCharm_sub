# Generated by Django 3.1.5 on 2021-01-27 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='special_offers',
            field=models.CharField(choices=[('student', 'student'), ('classroom_assistant', 'classroom assistant'), ('open_source', 'open source'), ('no_offers', 'no special offers')], default='no_offers', max_length=128),
        ),
    ]
