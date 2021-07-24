from django.urls import path
from MetioTube.profiles.views import profile_page, edit_profile
import MetioTube.profiles.signals

urlpatterns = (
    path('<int:pk>', profile_page, name='profile page'),
    path('edit/', edit_profile, name='edit profile'),
)
