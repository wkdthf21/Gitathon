# Generated by Django 2.1.2 on 2018-10-28 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamproject', '0002_auto_20181027_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='peopleNum',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
