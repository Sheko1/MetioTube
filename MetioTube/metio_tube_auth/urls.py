from django.urls import path

from MetioTube.metio_tube_auth.views import RegisterUserView, LoginUserView, user_logout

urlpatterns = (
    path('register/', RegisterUserView.as_view(), name='user register'),
    path('login/', LoginUserView.as_view(), name='user login'),
    path('logout/', user_logout, name='user logout')
)
