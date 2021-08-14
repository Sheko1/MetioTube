from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from MetioTube.core.validators import validate_video_file, validate_image

UserModel = get_user_model()


class Video(models.Model):
    title = models.CharField(
        max_length=30
    )

    description = models.TextField()

    thumbnail = CloudinaryField(
        resource_type='image',
        blank=True,
        validators=(validate_image,),
    )

    video_file = CloudinaryField(
        resource_type='video',
        validators=(validate_video_file,),
    )

    date = models.DateTimeField(
        auto_now_add=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class LikeDislike(models.Model):
    # 0 for dislike 1 for like
    like_or_dislike = models.IntegerField(
        help_text='1 for like 0 for dislike'
    )

    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class VideoView(models.Model):
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
    )

    session_key = models.CharField(
        max_length=32,
        blank=True
    )


class CommentVideo(models.Model):
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    date = models.DateTimeField(
        auto_now_add=True,
    )

    content = models.TextField()
