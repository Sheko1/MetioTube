import MetioTube.main_app.signals
from django.urls import path
from MetioTube.main_app.views import home_page, video_page, upload_video, like_dislike_video, edit_video, comment_video, \
    delete_comment, delete_video, subscribers

urlpatterns = (
    path('', home_page, name='home page'),
    path('video/<int:pk>', video_page, name='video page'),
    path('upload/', upload_video, name='upload video'),
    path('edit-video/<int:pk>', edit_video, name='edit video'),
    path('delete-video/<int:pk>', delete_video, name='delete video'),
    path('like_dislike/<int:pk>/<int:like_dislike>', like_dislike_video, name='like-dislike video'),
    path('comment-video/<int:pk>', comment_video, name='comment video'),
    path('delete-comment/<int:pk>', delete_comment, name='delete comment'),
    path('subscribers/', subscribers, name='subscribers page')
)
