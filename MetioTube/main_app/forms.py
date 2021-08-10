from django import forms

from MetioTube.main_app.models import Video, CommentVideo


class VideoUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['video_file'].widget.attrs['accept'] = 'video/mp4, video/avi, video/mov'
        self.fields['thumbnail'].widget.attrs['accept'] = 'image/jpg, image/png, image/jpeg'

    class Meta:
        model = Video
        fields = ('title', 'description', 'video_file', 'thumbnail')
        help_texts = {'video_file': 'Valid extensions: mp4, avi, mov', 'thumbnail': 'Can be blank'}


class VideoEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['thumbnail'].widget.attrs['accept'] = 'image/jpg, image/png, image/jpeg'

    class Meta:
        model = Video
        fields = ('title', 'description', 'thumbnail')
        help_texts = {'thumbnail': 'Can be blank'}


class CommentVideoForm(forms.ModelForm):
    class Meta:
        model = CommentVideo
        fields = ('content',)
