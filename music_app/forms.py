from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import MusicFile


class MusicFileForm(forms.ModelForm):
    class Meta:
        model = MusicFile
        fields = ('file', 'upload_type', 'allowed_emails')
        widgets = {
            'allowed_emails': forms.Textarea(attrs={'rows': 3}),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
