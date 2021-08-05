from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import DetailView

from MetioTube.main_app.models import Video
from MetioTube.profiles.forms import ProfileForm
from MetioTube.profiles.models import Profile


class ProfileDetailsView(DetailView):
    template_name = 'profiles/profile-page.html'
    model = Profile
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user
        context['videos'] = Video.objects.filter(user_id=self.kwargs['pk'])
        context['profile_page'] = True

        return context


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


@login_required
def subscribe(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    if request.user == profile.user:
        return redirect("profile page", pk)

    if request.user in profile.subscribers.all():
        profile.subscribers.remove(request.user)

    else:
        profile.subscribers.add(request.user)

    return redirect("profile page", pk)
