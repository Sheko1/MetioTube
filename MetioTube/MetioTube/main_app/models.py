from django.db import models

# Create your models here.
from MetioTube.main_app.validators import validate_video_file


class Video(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='images')
    video_file = models.FileField(
        validators=[validate_video_file],
        upload_to='videos'
    )
