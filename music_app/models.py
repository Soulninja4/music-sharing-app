from django.db import models
from django import forms
from django.contrib.auth.models import User


class MusicFile(models.Model):
    UPLOAD_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('protected', 'Protected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='music_files')
    upload_type = models.CharField(max_length=10, choices=UPLOAD_CHOICES)
    allowed_emails = models.TextField(blank=True)
    url = models.CharField(max_length=100, blank=True)

    # Add any other necessary fields

    def __str__(self):
        return self.file.name


class MusicFileForm(forms.ModelForm):
    class Meta:
        model = MusicFile
        fields = ('file', 'upload_type', 'allowed_emails')
        widgets = {
            'allowed_emails': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        upload_type = cleaned_data.get('upload_type')
        allowed_emails = cleaned_data.get('allowed_emails')

        if upload_type != 'protected' and allowed_emails:
            self.add_error(
                'allowed_emails', 'Allowed emails can only be used for protected uploads.')

        return cleaned_data
