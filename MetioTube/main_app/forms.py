from django import forms

from MetioTube.main_app.models import Video, CommentVideo


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'description', 'video_file', 'thumbnail')
        help_texts = {'video_file': 'Valid extensions: mp4, avi, mov', 'thumbnail': 'Can be blank'}


class VideoEditForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'description', 'thumbnail')
        help_texts = {'thumbnail': 'Can be blank'}


class CommentVideoForm(forms.ModelForm):
    class Meta:
        model = CommentVideo
        fields = ('content',)
