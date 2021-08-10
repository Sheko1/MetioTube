from unittest import mock

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files import File

from MetioTube.core.validators import validate_image


class ValidateImageTests(TestCase):
    def setUp(self):
        self.file = mock.MagicMock(spec=File)

    def test_validateImageWhenExtensionIsInvalid_expectToRaise(self):
        self.file.name = 'test.webp'

        with self.assertRaises(ValidationError) as context:
            validate_image(self.file)

        self.assertEqual('Wrong image extension! Valid extensions are: jpg, png, jpeg!', context.exception.message)

    def test_validateImageWhenSizeIsToBig_expectToRaise(self):
        self.file.name = 'test.jpg'
        self.file.size = 10485761

        with self.assertRaises(ValidationError) as context:
            validate_image(self.file)

        self.assertEqual('Max image size is 10MB', context.exception.message)

    def test_validateImageWhenIsValid_expectNothing(self):
        self.file.name = 'test.jpg'
        self.file.size = 123

        validate_image(self.file)
