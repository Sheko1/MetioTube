from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from MetioTube.metio_tube_auth.forms import RegisterForm


class RegisterUserView(CreateView):
    template_name = 'auth/user-register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home page')

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)

        return result


class LoginUserView(LoginView):
    template_name = 'auth/user-login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home page')

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('home page')


def user_logout(request):
    logout(request)
    return redirect('home page')
