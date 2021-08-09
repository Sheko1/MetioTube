import os.path

from django.core.exceptions import ValidationError


def validate_video_file(value):
    if hasattr(value, 'name'):
        extension = os.path.splitext(value.name)[1]
        valid_extensions = ('.mp4', '.avi', '.mov')

        if not extension.lower() in valid_extensions:
            raise ValidationError('Wrong video extension')

        if value.size > 104857600:
            raise ValidationError('Max video size is 100MB')


def validate_image(value):
    if hasattr(value, 'name'):
        extension = os.path.splitext(value.name)[1]
        valid_extensions = ('.jpg', '.png', '.jpeg')

        if not extension.lower() in valid_extensions:
            raise ValidationError('Wrong image extension')

        if value.size > 10485760:
            raise ValidationError('Max image size is 10MB')
