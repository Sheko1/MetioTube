from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from MetioTube.main_app.models import Video
from MetioTube.profiles.forms import ProfileForm
from MetioTube.profiles.models import Profile


def profile_page(request, pk):
    profile = Profile.objects.get(pk=pk)
    videos = Video.objects.filter(user_id=pk)

    context = {
        'profile': profile,
        'user': request.user,
        'videos': videos
    }

    return render(request, 'profiles/profile-page.html', context)


@login_required
def edit_profile(request):
    profile = Profile.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile page', profile.user_id)

    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form
    }

    return render(request, 'profiles/edit-profile.html', context)
