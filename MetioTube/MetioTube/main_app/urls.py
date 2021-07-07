from django.urls import path

from MetioTube.main_app.views import home_page, video_page, upload_video

urlpatterns = (
    path('', home_page, name='home page'),
    path('video/<int:pk>', video_page, name='video page'),
    path('upload/', upload_video, name='upload video'),
)
