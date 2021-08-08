from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from MetioTube.main_app.models import Video, LikeDislike, CommentVideo

UserModel = get_user_model()


class VideoDetailsViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@test.test',
            password='123',
        )
        self.video = Video.objects.create(
            title='test',
            description='test',
            video_file='test.mp4',
            user=self.user
        )

    def test_getVideoDetails_whenVideoExistsAndNotOwner_expectToReturnDetailsForNotOwner(self):
        response = self.client.get(reverse('video page', kwargs={'pk': self.video.id}))
        self.assertFalse(response.context['is_owner'])
        self.assertEqual(200, response.status_code)

    def test_getVideoDetails_whenVideoExistsAndIsOwner_expectToReturnDetailsForOwner(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('video page', kwargs={'pk': self.video.id}))
        self.assertTrue(response.context['is_owner'])
        self.assertEqual(200, response.status_code)

    def test_getVideoDetails_whenVideoHasLikesDislikesAndComments_expectToReturnLikesDislikesAndComments(self):
        LikeDislike.objects.create(
            like_or_dislike=1,
            video=self.video,
            user=self.user
        )

        LikeDislike.objects.create(
            like_or_dislike=0,
            video=self.video,
            user=self.user
        )

        comment = CommentVideo.objects.create(
            video=self.video,
            user=self.user,
            content='test'
        )

        response = self.client.get(reverse('video page', kwargs={'pk': self.video.id}))

        self.assertEqual(1, response.context['likes'])
        self.assertEqual(1, response.context['dislikes'])
        self.assertListEqual([comment], list(response.context['comments']))
        self.assertEqual(200, response.status_code)

    def test_getVideoDetails_expectViewCountToIncrease(self):
        self.assertEqual(0, self.video.videoview_set.count())
        response = self.client.get(reverse('video page', kwargs={'pk': self.video.id}))
        self.assertEqual(1, response.context['views'])
        self.assertEqual(200, response.status_code)

    def test_getVideoDetailsMoreThanOneTimeInLessThanHalfMin_expectViewCountToIncreaseOnce(self):
        self.assertEqual(0, self.video.videoview_set.count())
        self.client.get(reverse('video page', kwargs={'pk': self.video.id}))
        response = self.client.get(reverse('video page', kwargs={'pk': self.video.id}))
        self.assertEqual(1, response.context['views'])
        self.assertEqual(200, response.status_code)

    def test_getVideoDetailsWhenUserNotLikedOrDislike_expectIsRatedByUserToBeFalse(self):
        response = self.client.get(reverse('video page', kwargs={'pk': self.video.id}))
        self.assertFalse(response.context['is_rated_by_user'])
        self.assertEqual(200, response.status_code)

    def test_getVideoDetailsWhenUserLikedOrDisliked_expectIsRatedByUserToBeTrue(self):
        LikeDislike.objects.create(
            like_or_dislike=1,
            video=self.video,
            user=self.user
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse('video page', kwargs={'pk': self.video.id}))
        self.assertTrue(response.context['is_rated_by_user'])
        self.assertEqual(200, response.status_code)

    def test_getVideoDetailsWhenVideoPkIsNotValid_expectHttp404(self):
        response = self.client.get(reverse('video page', kwargs={'pk': 2}))
        self.assertEqual(404, response.status_code)
