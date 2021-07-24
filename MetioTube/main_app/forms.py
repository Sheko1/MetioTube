from django import forms

from MetioTube.main_app.models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'description', 'video_file', 'thumbnail')
