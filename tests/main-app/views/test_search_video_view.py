from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from MetioTube.main_app.models import Video

UserModel = get_user_model()


class SearchVideoViewTests(TestCase):
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

    def test_getSearchVideoWhenQueryDontMatchAnyVideos_expectNoneVideos(self):
        response = self.client.get(reverse('search video'), {'q': 'asd'})
        self.assertEqual(0, response.context['videos'].count())

        self.assertEqual(200, response.status_code)

    def test_getSearchVideoWhenQueryMatchVideo_expectVideos(self):
        response = self.client.get(reverse('search video'), {'q': 'test'})
        self.assertEqual(1, response.context['videos'].count())

        self.assertEqual(200, response.status_code)
