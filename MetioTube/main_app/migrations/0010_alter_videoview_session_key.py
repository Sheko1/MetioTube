# Generated by Django 3.2.5 on 2021-08-14 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_auto_20210809_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoview',
            name='session_key',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]
