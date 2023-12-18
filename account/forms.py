from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Password', required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']

    def clean_email(self):
        user_email = self.cleaned_data['email']
        try:
            User.objects.get(email=user_email)
        except User.DoesNotExist:
            return user_email
        else:
            raise forms.ValidationError('Email already in use')


class ProfileRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)

    class Meta:
        model = UserProfile
        fields = ['gender', 'date_of_birth', 'gender_preference', 'photo', 'about_me']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class RelationshipForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['relationship']


class InterestsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['interests']


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'date_of_birth', 'gender_preference',
                  'photo', 'about_me', 'relationship', 'interests']
