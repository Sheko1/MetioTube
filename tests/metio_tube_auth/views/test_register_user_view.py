from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core import mail
import threading

from MetioTube.profiles.models import Profile

UserModel = get_user_model()


class RegisterUserViewTests(TestCase):
    @staticmethod
    def wait_to_send_email():
        wait = True
        while wait:
            for thread in threading.enumerate():
                if thread.name == 'email_sender':
                    wait = True

                else:
                    wait = False

    def setUp(self):
        settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
        self.post_data = {'email': 'test@test.com', 'password1': 'test', 'password2': 'test'}

    def test_postRegisterUserWithValidPostData_expectToCreateNotActiveUser(self):
        self.assertEqual(0, UserModel.objects.all().count())
        response = self.client.post(reverse('user register'), self.post_data)
        self.assertEqual(1, UserModel.objects.all().count())
        self.assertFalse(UserModel.objects.all().first().is_active)

        self.assertEqual(200, response.status_code)

    def test_postRegisterUserWithValidPostData_expectToSendEmail(self):
        self.assertEqual(0, len(mail.outbox))
        response = self.client.post(reverse('user register'), self.post_data)
        self.wait_to_send_email()

        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(200, response.status_code)

    def test_postRegisterUserWhenClickActivateLink_expectToActivateAccount(self):
        self.client.post(reverse('user register'), self.post_data)
        self.assertFalse(UserModel.objects.all().first().is_active)

        self.wait_to_send_email()

        activation_link = 'http://'
        activation_link += mail.outbox[0].message().as_string().strip().split('\n')[-1].strip()
        response = self.client.get(activation_link)

        self.assertTrue(UserModel.objects.all().first().is_active)

        self.assertEqual(302, response.status_code)

    def test_postRegisterUserWhenClickActivationLinkWhenUserIsActivated_expectHttp404(self):
        self.client.post(reverse('user register'), self.post_data)
        self.wait_to_send_email()

        self.wait_to_send_email()

        activation_link = 'http://'
        activation_link += mail.outbox[0].message().as_string().strip().split('\n')[-1].strip()
        self.client.get(activation_link)
        response = self.client.get(activation_link)

        self.assertEqual(404, response.status_code)

    def test_RegisterUserWhenRegistered_expectToHaveProfile(self):
        user = UserModel.objects.create(
            email='test@test.test',
            password='test'
        )
        profile = Profile.objects.get(user=user)

        self.assertEqual(user, profile.user)
        self.assertEqual('test', profile.username)
