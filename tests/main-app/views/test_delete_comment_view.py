from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from MetioTube.main_app.models import Video, CommentVideo

UserModel = get_user_model()


class DeleteCommentViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@test.test',
            password='123',
        )

        self.user2 = UserModel.objects.create_user(
            email='test2@test.test',
            password='123',
        )

        self.user3 = UserModel.objects.create_user(
            email='test3@test.test',
            password='123',
        )

        self.video = Video.objects.create(
            title='test',
            description='test',
            video_file='test.mp4',
            user=self.user,
        )

        self.comment = CommentVideo.objects.create(
            video=self.video,
            user=self.user2,
            content='test'
        )

    def test_postDeleteCommentWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.post(reverse('delete comment', kwargs={'pk': self.comment.id}))
        self.assertEqual(302, response.status_code)

    def test_getDeleteCommentWhenAuthenticatedUser_expectHttp405(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('delete comment', kwargs={'pk': self.comment.id}))
        self.assertEqual(405, response.status_code)

    def test_postDeleteCommentWhenPkIsInvalid_expectHttp404(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete comment', kwargs={'pk': self.comment.id + 1}))
        self.assertEqual(404, response.status_code)

    def test_postDeleteCommentWhenUserIsOwner_expectToDelete(self):
        self.client.force_login(self.user2)
        self.assertEqual(1, CommentVideo.objects.filter(user=self.user2, video=self.video).count())

        response = self.client.post(reverse('delete comment', kwargs={'pk': self.comment.id}))
        self.assertEqual(0, CommentVideo.objects.filter(user=self.user2, video=self.video).count())

        self.assertEqual(302, response.status_code)

    def test_postDeleteCommentWhenUserIsOwnerOfVideo_expectToDelete(self):
        self.client.force_login(self.user)

        self.assertEqual(1, CommentVideo.objects.filter(user=self.user2, video=self.video).count())

        response = self.client.post(reverse('delete comment', kwargs={'pk': self.comment.id}))
        self.assertEqual(0, CommentVideo.objects.filter(user=self.user2, video=self.video).count())

        self.assertEqual(302, response.status_code)

    def test_postDeleteCommentWhenUserIsNotOwner_expectToNotDelete(self):
        self.client.force_login(self.user3)

        self.assertEqual(1, CommentVideo.objects.filter(user=self.user2, video=self.video).count())

        response = self.client.post(reverse('delete comment', kwargs={'pk': self.comment.id}))
        self.assertEqual(1, CommentVideo.objects.filter(user=self.user2, video=self.video).count())

        self.assertEqual(302, response.status_code)
