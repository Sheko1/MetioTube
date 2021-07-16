from django.urls import path

from MetioTube.metio_tube_auth.views import user_register, user_login, user_logout

urlpatterns = (
    path('register/', user_register, name='user register'),
    path('login/', user_login, name='user login'),
    path('logout/', user_logout, name='user logout')
)
