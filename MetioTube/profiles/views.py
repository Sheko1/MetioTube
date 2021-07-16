from django.shortcuts import render, redirect

# Create your views here.
from MetioTube.profiles.forms import ProfileForm
from MetioTube.profiles.models import Profile


def profile_page(request):
    profile = Profile.objects.get(pk=request.user.id)

    context = {
        'profile': profile
    }

    return render(request, 'profiles/profile-page.html', context)


def edit_profile(request):
    profile = Profile.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile page')

    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form
    }

    return render(request, 'profiles/edit-profile.html', context)
