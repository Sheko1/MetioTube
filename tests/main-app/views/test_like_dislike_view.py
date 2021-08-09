from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from MetioTube.main_app.models import Video, LikeDislike

UserModel = get_user_model()


class LikeDislikeViewTests(TestCase):
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

    def test_postLikeDislikeWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.post(reverse('like-dislike video', kwargs={'pk': self.video.id, 'like_dislike': 1}))
        self.assertEqual(302, response.status_code)

    def test_getLikeDislikeWhenAuthenticatedUser_expectHttp405(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('like-dislike video', kwargs={'pk': self.video.id, 'like_dislike': 1}))
        self.assertEqual(405, response.status_code)

    def test_postLikeDislikeWhenVideoPkIsInvalid_expectHttp404(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('like-dislike video', kwargs={'pk': self.video.id + 1, 'like_dislike': 1}))
        self.assertEqual(404, response.status_code)

    def test_postLikeDislikeWhenUserHasNoLikes_expectToLike(self):
        self.client.force_login(self.user)

        self.assertEqual(0, LikeDislike.objects.filter(user=self.user).count())
        response = self.client.post(reverse('like-dislike video', kwargs={'pk': self.video.id, 'like_dislike': 1}))
        self.assertEqual(1, LikeDislike.objects.filter(user=self.user).count())

        self.assertEqual(302, response.status_code)

    def test_postLikeDislikeWhenUserChangeFromLikeToDislike_expectToChangeToDislike(self):
        LikeDislike.objects.create(
            like_or_dislike=1,
            video=self.video,
            user=self.user
        )

        self.client.force_login(self.user)

        self.assertEqual(1, LikeDislike.objects.filter(like_or_dislike=1, user=self.user).count())
        self.assertEqual(0, LikeDislike.objects.filter(like_or_dislike=0, user=self.user).count())

        response = self.client.post(reverse('like-dislike video', kwargs={'pk': self.video.id, 'like_dislike': 0}))

        self.assertEqual(0, LikeDislike.objects.filter(like_or_dislike=1, user=self.user).count())
        self.assertEqual(1, LikeDislike.objects.filter(like_or_dislike=0, user=self.user).count())

        self.assertEqual(302, response.status_code)

    def test_postLikeDislikeWhenUserLikeAgain_expectToRemoveLike(self):
        LikeDislike.objects.create(
            like_or_dislike=1,
            video=self.video,
            user=self.user
        )

        self.client.force_login(self.user)
        self.assertEqual(1, LikeDislike.objects.filter(user=self.user).count())

        response = self.client.post(reverse('like-dislike video', kwargs={'pk': self.video.id, 'like_dislike': 1}))

        self.assertEqual(0, LikeDislike.objects.filter(user=self.user).count())

        self.assertEqual(302, response.status_code)

