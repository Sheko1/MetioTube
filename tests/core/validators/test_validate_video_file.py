from unittest import mock

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files import File

from MetioTube.core.validators import validate_video_file


class ValidateVideoFileTests(TestCase):
    def setUp(self):
        self.file = mock.MagicMock(spec=File)

    def test_validateVideoFileWhenExtensionIsInvalid_expectToRaise(self):
        self.file.name = 'test.mkv'

        with self.assertRaises(ValidationError) as context:
            validate_video_file(self.file)

        self.assertEqual('Wrong video extension! Valid extensions are: mp4, webm, mov!', context.exception.message)

    def test_validateVideoFileWhenSizeIsToBig_expectToRaise(self):
        self.file.name = 'test.mp4'
        self.file.size = 104857601

        with self.assertRaises(ValidationError) as context:
            validate_video_file(self.file)

        self.assertEqual('Max video size is 100MB', context.exception.message)

    def test_validateVideoFileWhenIsValid_expectNothing(self):
        self.file.name = 'test.mp4'
        self.file.size = 123
        validate_video_file(self.file)
