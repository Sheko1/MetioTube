from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class DeleteAccountViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@test.test',
            password='123',
        )
        self.user2 = UserModel.objects.create_user(
            email='test2@test.test',
            password='123',
        )

    def test_getDeleteAccountWhenUserIsNotOwner_expectHttp403(self):
        response = self.client.get(reverse('delete account', kwargs={'pk': self.user.id}))
        self.assertEqual(403, response.status_code)

        self.client.force_login(self.user2)

        response = self.client.get(reverse('delete account', kwargs={'pk': self.user.id}))
        self.assertEqual(403, response.status_code)

    def test_getDeleteAccountWhenUserIsOwner_expectSuccess(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('delete account', kwargs={'pk': self.user.id}))
        self.assertEqual(200, response.status_code)
