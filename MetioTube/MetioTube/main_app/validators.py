import os.path

from django.core.exceptions import ValidationError


def validate_video_file(value):
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ('.mp4', '.mkv', '.avi')

    if not extension.lower() in valid_extensions:
        raise ValidationError('Wrong file extension!')
