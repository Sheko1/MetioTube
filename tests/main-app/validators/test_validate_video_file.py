from unittest import mock

from django.core.exceptions import ValidationError
from django.core.files import File
from django.test import TestCase

from MetioTube.main_app.validators import validate_video_file


class ValidateVideoFileTests(TestCase):
    def test_ValidateVideoFileWhenFileHasInvalidExtension_expectToRaise(self):
        video_file = mock.MagicMock(spec=File)
        video_file.name = 'test.mkv'

        with self.assertRaises(ValidationError) as context:
            validate_video_file(video_file)

    def test_ValidateVideoFileWhenFileHasValidExtension_expectSuccess(self):
        video_file = mock.MagicMock(spec=File)
        video_file.name = 'test.mp4'
        result = validate_video_file(video_file)

        self.assertIsNone(result)
