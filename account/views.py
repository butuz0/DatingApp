from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import UserRegistrationForm, ProfileRegistrationForm, LoginForm
from .models import Profile


# Create your views here.
def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            Profile.objects.create(user=new_user)
            return redirect(reverse('account:profile_register'))
    else:
        form = UserRegistrationForm()
    return render(request, 'account/user_register.html', {'form': form})


@login_required
def profile_registration(request):
    if request.method == 'POST':
        form = ProfileRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            user = request.user
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()

            profile = Profile.objects.get(user=user)
            profile.gender = cd['gender']
            profile.date_of_birth = cd['date_of_birth']
            profile.photo = cd['photo']
            profile.preferences = cd['preferences']
            profile.save()

            return render(request, 'account/registration_done.html', {'profile': profile})
    else:
        form = ProfileRegistrationForm()
    return render(request, 'account/profile_register.html', {'form': form})
