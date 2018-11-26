# Generated by Django 2.1.3 on 2018-11-26 22:24

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hackathon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('memberId', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=40)),
                ('registerDate', models.DateTimeField(default=datetime.datetime(2018, 11, 26, 22, 24, 31, 964885, tzinfo=utc), verbose_name='date registered')),
            ],
        ),
        migrations.CreateModel(
            name='Participate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hackId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hackathon.HackathonInformation')),
                ('memberId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Member')),
            ],
        ),
    ]
