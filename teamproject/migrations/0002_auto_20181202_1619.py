# Generated by Django 2.1.3 on 2018-12-02 07:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamproject', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamnotice',
            name='writtenDate',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 2, 7, 19, 18, 336543, tzinfo=utc), verbose_name='date registered'),
        ),
    ]
