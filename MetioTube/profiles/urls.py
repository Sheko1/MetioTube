from django.urls import path
from MetioTube.profiles.views import profile_page, edit_profile, subscribe
import MetioTube.profiles.signals

urlpatterns = (
    path('<int:pk>', profile_page, name='profile page'),
    path('edit/', edit_profile, name='edit profile'),
    path('subscribe/<int:pk>', subscribe, name='subscribe')
)
