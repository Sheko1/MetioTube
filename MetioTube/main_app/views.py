from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from MetioTube.core.get_view import get_view
from MetioTube.core.views_mixin import OwnerOfContentRequiredMixin
from MetioTube.main_app.forms import VideoUploadForm, VideoEditForm, CommentVideoForm
from MetioTube.main_app.models import Video, LikeDislike, CommentVideo
from MetioTube.profiles.models import Profile

UserModel = get_user_model()


class HomeListView(ListView):
    template_name = 'metio-tube/index.html'
    model = Video
    context_object_name = 'videos'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('?')


class VideoDetailsView(DetailView):
    template_name = 'metio-tube/video-details.html'
    model = Video
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile'] = Profile.objects.get(pk=self.object.user_id)
        context['comments'] = self.object.commentvideo_set.order_by('-date')
        context['likes'] = self.object.likedislike_set.filter(like_or_dislike=1).count()
        context['dislikes'] = self.object.likedislike_set.filter(like_or_dislike=0).count()
        context['is_rated_by_user'] = self.object.likedislike_set.filter(user_id=self.request.user.id).first()
        context['views'] = self.object.videoview_set.count()
        context['is_owner'] = self.request.user == self.object.user

        return context

    def dispatch(self, request, *args, **kwargs):
        if self.get_object():
            get_view(request, kwargs['pk'])

        return super().dispatch(request, *args, **kwargs)


class UploadVideoView(LoginRequiredMixin, CreateView):
    template_name = 'metio-tube/upload-video.html'
    form_class = VideoUploadForm
    success_url = reverse_lazy('home page')

    def form_valid(self, form):
        video = form.save(commit=False)
        video.user = self.request.user
        video.save()

        return super().form_valid(form)


class EditVideoView(LoginRequiredMixin, OwnerOfContentRequiredMixin, UpdateView):
    template_name = 'metio-tube/edit-video.html'
    model = Video
    form_class = VideoEditForm

    def get_success_url(self):
        return reverse('video page', kwargs={'pk': self.object.id})


class DeleteVideoView(LoginRequiredMixin, OwnerOfContentRequiredMixin, DeleteView):
    template_name = 'metio-tube/delete-video.html'
    model = Video
    success_url = reverse_lazy('home page')


class LikeDislikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        video = get_object_or_404(Video, pk=kwargs['pk'])
        user_like = video.likedislike_set.filter(user=request.user)

        if user_like:
            user_like = user_like.get()
            user_like.delete()

            if user_like.like_or_dislike == kwargs['like_dislike']:
                return redirect('video page', kwargs['pk'])

        LikeDislike(
            like_or_dislike=kwargs['like_dislike'],
            user=request.user,
            video=video
        ).save()

        return redirect('video page', kwargs['pk'])


class CommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        video = get_object_or_404(Video, pk=kwargs['pk'])
        form = CommentVideoForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = video
            comment.user = request.user
            comment.save()

        return redirect('video page', kwargs['pk'])


class DeleteCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(CommentVideo, pk=kwargs['pk'])

        if request.user == comment.user or request.user == comment.video.user:
            comment.delete()

        return redirect('video page', comment.video_id)


class SubscribersView(LoginRequiredMixin, ListView):
    template_name = 'metio-tube/subscriptions.html'
    context_object_name = 'videos'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['subscriptions'] = self.request.user.subscribers.all()

        return context

    def get_queryset(self):
        subscriptions = self.request.user.subscribers.all()
        videos = Video.objects.none()

        for profile in subscriptions:
            videos = videos.union(Video.objects.filter(user=profile.user))

        return videos.order_by('-date')


class SearchVideoView(ListView):
    template_name = 'metio-tube/index.html'
    context_object_name = 'videos'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')

        return context

    def get_queryset(self):
        return Video.objects.filter(title__icontains=self.request.GET.get('q'))
