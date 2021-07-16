from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

# Create your views here.
from MetioTube.metio_tube_auth.forms import RegisterForm, LoginForm


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('user login')

    else:
        form = RegisterForm()

    context = {
        'form': form
    }

    return render(request, 'auth/user-register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home page')

    else:
        form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, 'auth/user-login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home page')
