from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class EditProfileTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@test.test',
            password='123',
        )

    def test_getEditProfileWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.get(reverse('edit profile'))
        self.assertEqual(302, response.status_code)

    def test_postEditProfileWhenPostDataIsValid_expectToChange(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('edit profile'), {'username': 'test2'})
        self.assertNotEqual(self.user.profile.username, UserModel.objects.get(pk=self.user.id).profile.username)
        self.assertEqual(302, response.status_code)
