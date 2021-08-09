# Generated by Django 3.2.5 on 2021-08-03 16:08

import MetioTube.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_commentvideo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_file',
            field=models.FileField(upload_to='videos', validators=[MetioTube.core.validators.validate_video_file]),
        ),
    ]
