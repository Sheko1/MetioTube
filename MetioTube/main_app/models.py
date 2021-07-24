from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from MetioTube.main_app.validators import validate_video_file

UserModel = get_user_model()


class Video(models.Model):
    title = models.CharField(
        max_length=30
    )

    description = models.TextField()

    thumbnail = models.ImageField(
        upload_to='images',
        blank=True,
        help_text='Can be blank'
    )

    video_file = models.FileField(
        validators=[validate_video_file],
        upload_to='videos',
        help_text='Valid extensions: mp4, mkv, avi'
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )
