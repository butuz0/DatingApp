from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import UserRegistrationForm, ProfileRegistrationForm, LoginForm
from .models import UserProfile


# Create your views here.
def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect(reverse('account:profile_register'))
    else:
        form = UserRegistrationForm()
    return render(request, 'account/user_register.html', {'form': form})


@login_required
def profile_registration(request):
    if request.method == 'POST':
        form = ProfileRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data

            user = request.user
            login(request, user)
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()

            profile = UserProfile.objects.create(user=user,
                                                 gender=cd['gender'],
                                                 date_of_birth=cd['date_of_birth'],
                                                 photo=cd['photo'],
                                                 preferences=cd['preferences'],
                                                 about_me=cd['about_me'])
            profile.save()

            return render(request, 'account/registration_done.html', {'profile': profile})
    else:
        form = ProfileRegistrationForm()
    return render(request, 'account/profile_register.html', {'form': form})
