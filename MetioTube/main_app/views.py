from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from MetioTube.main_app.forms import VideoForm
from MetioTube.main_app.models import Video
from MetioTube.profiles.models import Profile

UserModel = get_user_model()


def home_page(request):
    videos = Video.objects.all()

    context = {
        'videos': videos
    }

    return render(request, 'metio-tube/home-page.html', context)


def video_page(request, pk):
    video = Video.objects.get(pk=pk)
    profile = Profile.objects.get(pk=video.user.id)

    context = {
        'video': video,
        'profile': profile,
    }

    return render(request, 'metio-tube/video-page.html', context)


@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)

        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return redirect('home page')

    else:
        form = VideoForm()

    context = {
        'form': form
    }

    return render(request, 'metio-tube/upload-video.html', context)
