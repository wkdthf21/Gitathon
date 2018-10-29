# Generated by Django 2.1.2 on 2018-10-28 14:10

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0020_auto_20181028_2305'),
        ('accounts', '0005_auto_20181027_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='participate',
            name='hackId',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='hackathon.HackathonInformation'),
        ),
        migrations.AlterField(
            model_name='member',
            name='registerDate',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 28, 14, 10, 18, 330160, tzinfo=utc), verbose_name='date registered'),
        ),
    ]
