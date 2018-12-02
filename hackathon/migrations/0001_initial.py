# Generated by Django 2.1.3 on 2018-12-02 07:17

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HackathonInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('applyDate_start', models.DateField(help_text='Please use the following format : <em>YYYY-MM-DD</em>')),
                ('applyTime_start', models.TimeField(help_text='Please use the following format : <em>12:00:00</em>')),
                ('applyDate_end', models.DateField(help_text='Please use the following format : <em>YYYY-MM-DD</em>')),
                ('applyTime_end', models.TimeField(help_text='Please use the following format : <em>12:00:00</em>')),
                ('contestDate_start', models.DateField(help_text='Please use the following format : <em>YYYY-MM-DD</em>')),
                ('contestTime_start', models.TimeField(help_text='Please use the following format : <em>12:00:00</em>')),
                ('contestDate_end', models.DateField(help_text='Please use the following format : <em>YYYY-MM-DD</em>')),
                ('contestTime_end', models.TimeField(help_text='Please use the following format : <em>12:00:00</em>')),
                ('applyNum', models.IntegerField(default=0)),
                ('peopleNum', models.IntegerField()),
                ('memberNum_max', models.IntegerField()),
                ('memberNum_min', models.IntegerField()),
                ('selectMatching', models.IntegerField(choices=[(0, '자율선택'), (1, '랜덤매칭')])),
                ('Images', models.ImageField(upload_to='uploads/%Y/%m/%d')),
                ('text', models.TextField(blank=True)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('hackathonHost', models.CharField(default='none', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='HackNotice',
            fields=[
                ('hackNoticeId', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(default=datetime.datetime(2018, 12, 2, 7, 17, 36, 662237, tzinfo=utc))),
                ('hackId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon.HackathonInformation')),
            ],
        ),
    ]
