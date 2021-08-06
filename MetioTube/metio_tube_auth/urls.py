from django.urls import path

from MetioTube.metio_tube_auth.views import RegisterUserView, LoginUserView, user_logout, activate_account, \
    ForgotPasswordView, \
    ResetPasswordView, DeleteAccountView

urlpatterns = (
    path('register/', RegisterUserView.as_view(), name='user register'),
    path('login/', LoginUserView.as_view(), name='user login'),
    path('logout/', user_logout, name='user logout'),
    path('activate/<int:pk>/<token>', activate_account, name='activate'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot password'),
    path('reset-password/<int:pk>/<token>', ResetPasswordView.as_view(), name='reset password'),
    path('delete/<int:pk>', DeleteAccountView.as_view(), name='delete account')
)
