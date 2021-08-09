from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from MetioTube.core.validators import validate_image

UserModel = get_user_model()


class Profile(models.Model):
    username = models.CharField(
        max_length=30
    )

    profile_picture = CloudinaryField(
        resource_type='image',
        blank=True,
        validators=(validate_image,)
    )

    about = models.TextField(
        blank=True
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True
    )

    subscribers = models.ManyToManyField(
        UserModel,
        related_name='subscribers',
        blank=True,
    )

    def __str__(self):
        return self.username
