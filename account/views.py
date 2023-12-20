from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import UserRegistrationForm, ProfileRegistrationForm, LoginForm, RelationshipForm, InterestsForm, \
    UserSettingsForm, ProfileSettingsForm
from .models import UserProfile, GroupOfInterests


# Create your views here.
def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
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
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()

            profile = UserProfile.objects.create(user=user,
                                                 gender=cd['gender'],
                                                 date_of_birth=cd['date_of_birth'],
                                                 photo=cd['photo'],
                                                 gender_preference=cd['gender_preference'],
                                                 about_me=cd['about_me'])
            profile.save()
            return redirect(reverse('account:relationship_form'))
    else:
        form = ProfileRegistrationForm()
    return render(request, 'account/profile_register.html', {'form': form})


@login_required
def relationship_type_form(request):
    if request.method == 'POST':
        form = RelationshipForm(request.POST, instance=UserProfile.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            return redirect(reverse('account:interests_form'))
    else:
        form = RelationshipForm()
    return render(request, 'account/relationship_form.html', {'form': form})


@login_required
def interests_form(request):
    if request.method == 'POST':
        form = InterestsForm(request.POST, instance=UserProfile.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            return render(request, 'account/registration_done.html')
    else:
        form = InterestsForm()
    groups = GroupOfInterests.objects.all()
    return render(request, 'account/interests_form.html', {'form': form, 'groups': groups})


@login_required
def user_settings(request):
    user_form = UserSettingsForm(instance=request.user)
    profile_form = ProfileSettingsForm(instance=request.user.user_info)

    if request.method == 'POST':
        user_form = UserSettingsForm(request.POST, instance=request.user)
        profile_form = ProfileSettingsForm(request.POST, instance=request.user.user_info)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your settings have been updated successfully.')
            return redirect('account:settings')

    return render(request, 'account/settings.html', {'user_form': user_form,
                                                     'profile_form': profile_form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        print(f'user to delete: {user}')
        # user.delete()
        return redirect('home_page')

    return render(request, 'account/delete_account.html')
