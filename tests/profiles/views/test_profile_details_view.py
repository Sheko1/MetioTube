from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class ProfileDetailsViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@test.test',
            password='123',
        )

    def test_getProfileDetailsWhenPkNotValid_expectHttp404(self):
        response = self.client.get(reverse('profile page', kwargs={'pk': self.user.id + 1}))
        self.assertEqual(404, response.status_code)

    def test_getProfileDetailsWhenPkIsValid_expectSuccess(self):
        response = self.client.get(reverse('profile page', kwargs={'pk': self.user.id}))

        self.assertEqual(self.user.id, response.context['profile'].user_id)
        self.assertEqual(200, response.status_code)
