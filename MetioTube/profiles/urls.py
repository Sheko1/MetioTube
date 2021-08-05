from django.urls import path
from MetioTube.profiles.views import ProfileDetailsView, edit_profile, subscribe
import MetioTube.profiles.signals

urlpatterns = (
    path('<int:pk>', ProfileDetailsView.as_view(), name='profile page'),
    path('edit/', edit_profile, name='edit profile'),
    path('subscribe/<int:pk>', subscribe, name='subscribe')
)
