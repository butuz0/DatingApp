from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords do not match')
            return cd['password2']

        def clean_email(self):
            user_email = self.cleaned_data['email']
            if User.objects.get(email=user_email):
                raise forms.ValidationError('Email already in user')
            return user_email


class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'date_of_birth', 'preferences', 'photo']
