from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

UserModel = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email',)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        email = self.cleaned_data['email']
        if not UserModel.objects.filter(email=email):
            raise ValidationError('Email not found!')

        return super().clean()
