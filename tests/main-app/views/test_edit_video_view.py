from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from MetioTube.main_app.models import Video

UserModel = get_user_model()


class EditVideoViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@test.test',
            password='123',
        )

        self.user2 = UserModel.objects.create_user(
            email='test2@test.test',
            password='123',
        )

        self.video = Video.objects.create(
            title='test',
            description='test',
            video_file='test.mp4',
            user=self.user,
        )

    def test_getEditVideoWhenNotAuthenticatedUser_expectRedirect(self):
        response = self.client.get(reverse('edit video', kwargs={'pk': self.video.id}))
        self.assertEqual(302, response.status_code)

    def test_getEditVideoWhenAuthenticatedUserAndNotOwner_expectHttp403(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse('edit video', kwargs={'pk': self.video.id}))
        self.assertEqual(403, response.status_code)

    def test_getEditVideoWhenAuthenticatedUserAndOwner_expectSuccess(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit video', kwargs={'pk': self.video.id}))
        self.assertEqual(200, response.status_code)
