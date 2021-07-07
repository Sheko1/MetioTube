from django.shortcuts import render, redirect

# Create your views here.
from MetioTube.main_app.forms import VideoForm
from MetioTube.main_app.models import Video


def home_page(request):
    videos = Video.objects.all()

    context = {
        'videos': videos
    }

    return render(request, 'home-page.html', context)


def video_page(request, pk):
    video = Video.objects.get(pk=pk)

    context = {
        'video': video
    }

    return render(request, 'video-page.html', context)


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('home page')

    else:
        form = VideoForm()

    context = {
        'form': form
    }

    return render(request, 'upload-video.html', context)
