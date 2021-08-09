from django.urls import path
from MetioTube.main_app.views import HomeListView, UploadVideoView, LikeDislikeView, EditVideoView, \
    CommentView, \
    DeleteCommentView, DeleteVideoView, SubscribersView, VideoDetailsView, SearchVideoView

urlpatterns = (
    path('', HomeListView.as_view(), name='home page'),
    path('video/<int:pk>', VideoDetailsView.as_view(), name='video page'),
    path('upload/', UploadVideoView.as_view(), name='upload video'),
    path('edit-video/<int:pk>', EditVideoView.as_view(), name='edit video'),
    path('delete-video/<int:pk>', DeleteVideoView.as_view(), name='delete video'),
    path('like_dislike/<int:pk>/<int:like_dislike>', LikeDislikeView.as_view(), name='like-dislike video'),
    path('comment-video/<int:pk>', CommentView.as_view(), name='comment video'),
    path('delete-comment/<int:pk>', DeleteCommentView.as_view(), name='delete comment'),
    path('subscribers/', SubscribersView.as_view(), name='subscribers page'),
    path('search/', SearchVideoView.as_view(), name='search video'),
)
