from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from MetioTube.main_app.core.get_view import get_view
from MetioTube.main_app.forms import VideoForm
from MetioTube.main_app.models import Video, LikeDislike
from MetioTube.profiles.models import Profile

UserModel = get_user_model()


def home_page(request):
    videos = Video.objects.all()

    context = {
        'videos': videos,
    }

    return render(request, 'metio-tube/home-page.html', context)


def video_page(request, pk):
    get_view(request, pk)
    video = Video.objects.get(pk=pk)
    profile = Profile.objects.get(pk=video.user.id)

    likes = video.likedislike_set.filter(like_or_dislike=1).count()
    dislikes = video.likedislike_set.filter(like_or_dislike=0).count()
    is_rated = video.likedislike_set.filter(user_id=request.user.id)
    views = video.videoview_set.count()

    if is_rated:
        is_rated = is_rated.get()

    context = {
        'video': video,
        'profile': profile,
        'likes': likes,
        'dislikes': dislikes,
        'is_rated': is_rated,
        'views': views,
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


@login_required
def like_dislike_video(request, pk, like_dislike):
    video = Video.objects.get(pk=pk)
    user_like = video.likedislike_set.filter(user=request.user)

    if user_like:
        user_like = user_like.get()
        user_like.delete()

        if user_like.like_or_dislike == like_dislike:
            return redirect('video page', pk)

    LikeDislike(
        like_or_dislike=like_dislike,
        user=request.user,
        video=video
    ).save()

    return redirect('video page', pk)
