from django import forms

from MetioTube.profiles.models import Profile


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs['accept'] = 'image/jpg, image/png, image/jpeg'

    class Meta:
        model = Profile
        exclude = ('user', 'subscribers')
