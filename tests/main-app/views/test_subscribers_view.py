from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from MetioTube.main_app.models import Video

UserModel = get_user_model()


class SubscribersViewTests(TestCase):
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

    def test_getSubscribersWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.get(reverse('subscribers page'))
        self.assertEqual(302, response.status_code)

    def test_getSubscribersWhenAuthenticatedUser_expectSuccess(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('subscribers page'))
        self.assertEqual(200, response.status_code)

    def test_getSubscribersWhenUserHasNoSubscriptions_expectNoneSubscriptions(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('subscribers page'))

        self.assertEqual(0, response.context['subscriptions'].count())
        self.assertEqual(200, response.status_code)

    def test_getSubscribersWhenUserHasSubscriptionButHasNoVideos_expectToHaveSubscriptionWithoutVideos(self):
        self.client.force_login(self.user)
        self.user2.profile.subscribers.add(self.user)

        response = self.client.get(reverse('subscribers page'))

        self.assertEqual(1, response.context['subscriptions'].count())
        self.assertEqual(0, response.context['videos'].count())
        self.assertEqual(200, response.status_code)

    def test_getSubscribersWhenUserHasSubscriptionWithVideos_expectToHaveSubscriptionWithVideos(self):
        self.client.force_login(self.user2)
        self.user.profile.subscribers.add(self.user2)

        response = self.client.get(reverse('subscribers page'))

        self.assertEqual(1, response.context['subscriptions'].count())
        self.assertEqual(1, response.context['videos'].count())
        self.assertEqual(200, response.status_code)
