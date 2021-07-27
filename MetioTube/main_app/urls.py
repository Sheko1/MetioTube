import MetioTube.main_app.signals
from django.urls import path
from MetioTube.main_app.views import home_page, video_page, upload_video, like_dislike_video

urlpatterns = (
    path('', home_page, name='home page'),
    path('video/<int:pk>', video_page, name='video page'),
    path('upload/', upload_video, name='upload video'),
    path('like_dislike/<int:pk>/<int:like_dislike>', like_dislike_video, name='like-dislike video'),
)
