import os.path

from django.core.exceptions import ValidationError
from django.core.files import File


def validate_video_file(value):
    if isinstance(value, File):
        extension = os.path.splitext(value.name)[1]
        valid_extensions = ('.mp4', '.webm', '.mov')

        if not extension.lower() in valid_extensions:
            raise ValidationError('Wrong video extension! Valid extensions are: mp4, webm, mov!')

        if value.size > 104857600:
            raise ValidationError('Max video size is 100MB')


def validate_image(value):
    if isinstance(value, File):
        extension = os.path.splitext(value.name)[1]
        valid_extensions = ('.jpg', '.png', '.jpeg')

        if not extension.lower() in valid_extensions:
            raise ValidationError('Wrong image extension! Valid extensions are: jpg, png, jpeg! ')

        if value.size > 10485760:
            raise ValidationError('Max image size is 10MB')
