from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

UserModel = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email',)


class LoginForm(forms.Form):
    user = None

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def clean(self):
        self.user = authenticate(
            username=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        if not self.user:
            raise ValidationError('Wrong email or password')

    def get_user(self):
        return self.user

