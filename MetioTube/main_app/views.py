from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from MetioTube.main_app.core.get_view import get_view
from MetioTube.main_app.forms import VideoUploadForm, VideoEditForm, CommentVideoForm
from MetioTube.main_app.models import Video, LikeDislike, CommentVideo
from MetioTube.profiles.models import Profile

UserModel = get_user_model()


def home_page(request):
    videos = Video.objects.all()

    context = {
        'videos': videos,
    }

    return render(request, 'metio-tube/home-page.html', context)


def video_page(request, pk):
    video = get_object_or_404(Video, pk=pk)
    get_view(request, pk)
    profile = Profile.objects.get(pk=video.user.id)

    comments = video.commentvideo_set.order_by('-date')
    comment_form = CommentVideoForm()

    likes = video.likedislike_set.filter(like_or_dislike=1).count()
    dislikes = video.likedislike_set.filter(like_or_dislike=0).count()
    is_rated_by_user = video.likedislike_set.filter(user_id=request.user.id).first()
    views = video.videoview_set.count()
    is_owner = request.user == video.user

    context = {
        'video': video,
        'profile': profile,
        'likes': likes,
        'dislikes': dislikes,
        'is_rated_by_user': is_rated_by_user,
        'views': views,
        'is_owner': is_owner,
        'comments': comments,
        'form': comment_form,
    }

    return render(request, 'metio-tube/video-page.html', context)


@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)

        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return redirect('home page')

    else:
        form = VideoUploadForm()

    context = {
        'form': form
    }

    return render(request, 'metio-tube/upload-video.html', context)


@login_required
def like_dislike_video(request, pk, like_dislike):
    video = get_object_or_404(Video, pk=pk)
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


@login_required
def edit_video(request, pk):
    video = get_object_or_404(Video, pk=pk)

    if request.user != video.user:
        return redirect('video page', pk)

    if request.method == 'POST':
        form = VideoEditForm(request.POST, request.FILES, instance=video)

        if form.is_valid():
            form.save()
            return redirect('video page', pk)

    else:
        form = VideoEditForm(instance=video)

    context = {
        'form': form,
        'video_id': video.id
    }

    return render(request, 'metio-tube/edit-video.html', context)


@login_required
def comment_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    form = CommentVideoForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.video = video
        comment.user = request.user
        comment.save()

    return redirect('video page', pk)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(CommentVideo, pk=pk)

    if request.user == comment.user or request.user == comment.video.user:
        comment.delete()

    return redirect('video page', comment.video_id)
