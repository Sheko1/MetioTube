from unittest import mock

from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import TestCase
from django.urls import reverse

from MetioTube.main_app.models import Video

UserModel = get_user_model()


class UploadVideoViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@test.test',
            password='123',
        )

        self.post_data = {'title': 'test', 'description': 'test', 'video_file': '', 'user': self.user}

    def test_getUploadVideoWhenNotAuthenticatedUser_expectRedirect(self):
        response = self.client.get(reverse('upload video'))
        self.assertEqual(302, response.status_code)

    def test_getUploadVideoWhenAuthenticatedUser_expectSuccess(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('upload video'))
        self.assertEqual(200, response.status_code)

    def test_postUploadVideoWhenNotValidPostData_expectToNotCreateVideo(self):
        self.client.force_login(self.user)
        self.assertEqual(0, Video.objects.all().count())

        video_file = mock.MagicMock(spec=File)
        video_file.name = 'test.mp3'
        self.post_data['video_file'] = video_file

        self.client.post(reverse('upload video'), self.post_data)
        self.assertEqual(0, Video.objects.all().count())

    def test_postUploadVideoWhenValidPostData_expectToCreateVideoAndRedirect(self):
        self.client.force_login(self.user)
        self.assertEqual(0, Video.objects.all().count())

        video_file = mock.MagicMock(spec=File)
        video_file.name = 'test.mp4'
        self.post_data['video_file'] = video_file

        response = self.client.post(reverse('upload video'), self.post_data)
        self.assertEqual(1, Video.objects.all().count())
        self.assertEqual(302, response.status_code)
