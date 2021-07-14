from django import forms

from MetioTube.main_app.models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control mb-5 mt-2'
