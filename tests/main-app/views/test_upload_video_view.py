from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


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

