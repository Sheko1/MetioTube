from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from MetioTube.main_app.models import Video, CommentVideo

UserModel = get_user_model()


class CommentViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@test.test',
            password='123',
        )

        self.video = Video.objects.create(
            title='test',
            description='test',
            video_file='test.mp4',
            user=self.user,
        )
        self.post_data = {'content': 'test'}

    def test_postCommentWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.post(reverse('comment video', kwargs={'pk': self.video.id}), self.post_data)
        self.assertEqual(302, response.status_code)

    def test_getCommentWhenAuthenticatedUser_expectHttp405(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('comment video', kwargs={'pk': self.video.id}))
        self.assertEqual(405, response.status_code)

    def test_postCommentWhenVideoPkIsInvalid_expectHttp404(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('comment video', kwargs={'pk': self.video.id + 1}), self.post_data)
        self.assertEqual(404, response.status_code)

    def test_postCommentWithValidData_expectToCreate(self):
        self.client.force_login(self.user)

        self.assertEqual(0, CommentVideo.objects.filter(user=self.user).count())
        response = self.client.post(reverse('comment video', kwargs={'pk': self.video.id}), self.post_data)
        self.assertEqual(1, CommentVideo.objects.filter(user=self.user).count())

        self.assertEqual(302, response.status_code)

