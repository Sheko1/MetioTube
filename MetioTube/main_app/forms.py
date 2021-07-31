from django import forms

from MetioTube.main_app.models import Video, CommentVideo


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'description', 'video_file', 'thumbnail')


class VideoEditForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'description', 'thumbnail')


class CommentVideoForm(forms.ModelForm):
    class Meta:
        model = CommentVideo
        fields = ('content',)
