from threading import Thread

from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, DeleteView

from MetioTube.core.send_email import send_email
from MetioTube.core.views_mixin import UserAuthenticatedRedirectHomeMixin, ValidTokenLinkMixin
from MetioTube.metio_tube_auth.forms import RegisterForm, ForgotPasswordForm

UserModel = get_user_model()


class RegisterUserView(UserAuthenticatedRedirectHomeMixin, CreateView):
    template_name = 'auth/user-register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        Thread(
            name='email_sender',
            target=send_email,
            args=(user, self.request, 'Activate your account!', 'email-messages/activate-account-message.html')
        ).start()

        context = {
            'message': 'Please confirm your email address to complete the registration!'
        }

        return render(self.request, 'auth/email-sent.html', context)


class LoginUserView(UserAuthenticatedRedirectHomeMixin, LoginView):
    template_name = 'auth/user-login.html'

    def get_success_url(self):
        return reverse('home page')


class ForgotPasswordView(FormView):
    template_name = 'auth/forgot-password.html'
    form_class = ForgotPasswordForm

    def form_valid(self, form):
        user = UserModel.objects.get(email=form.cleaned_data['email'])

        Thread(
            target=send_email,
            args=(user, self.request, 'Password reset!', 'email-messages/reset-password-message.html')
        ).start()

        context = {
            'message': 'Email with reset link has been sent!'
        }

        return render(self.request, 'auth/email-sent.html', context)


class ResetPasswordView(ValidTokenLinkMixin, FormView):
    template_name = 'auth/reset-password.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('user login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = UserModel.objects.get(pk=self.kwargs['pk'])

        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DeleteAccountView(DeleteView):
    template_name = 'auth/delete-account.html'
    model = UserModel
    success_url = reverse_lazy('home page')

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user:
            return HttpResponse(status=403)

        return super().dispatch(request, *args, **kwargs)


def user_logout(request):
    logout(request)
    return redirect('home page')


def activate_account(request, pk, token):
    try:
        user = UserModel.objects.get(pk=pk)
    except UserModel.DoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('profile page', user.id)

    else:
        return HttpResponse(status=404)
