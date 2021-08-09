from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class SubscribeViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@test.test',
            password='123',
        )

        self.user2 = UserModel.objects.create_user(
            email='test2@test.test',
            password='123',
        )

    def test_getSubscribe_expectHttp405(self):
        response = self.client.get(reverse('subscribe', kwargs={'pk': self.user.id}))
        self.assertEqual(405, response.status_code)

    def test_postSubscribeWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.post(reverse('subscribe', kwargs={'pk': self.user.id}))
        self.assertEqual(302, response.status_code)

    def test_postSubscribeWhenUserIsOwner_expectNotToAddSubscription(self):
        self.client.force_login(self.user)

        self.assertEqual(0, self.user.subscribers.all().count())
        response = self.client.post(reverse('subscribe', kwargs={'pk': self.user.id}))
        self.assertEqual(0, UserModel.objects.get(pk=self.user.id).subscribers.all().count())

        self.assertEqual(302, response.status_code)

    def test_postSubscribeWhenUserIsNotOwner_expectToAddSubscription(self):
        self.client.force_login(self.user)

        self.assertEqual(0, self.user.subscribers.all().count())
        response = self.client.post(reverse('subscribe', kwargs={'pk': self.user2.id}))
        self.assertEqual(1, UserModel.objects.get(pk=self.user.id).subscribers.all().count())

        self.assertEqual(302, response.status_code)
