from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from account.models import UserProfile, Like, Report
from account.forms import ReportForm
from datetime import datetime
from django.utils import timezone
import requests
import json


# Create your views here.
@login_required
def list_people(request):
    current_user = request.user.user_info

    # filter people by preferences
    people = (UserProfile.objects.filter(gender_preference__in=[current_user.gender, 'BOTH'])
              .exclude(user=request.user))

    if current_user.gender_preference != 'BOTH':
        people = people.filter(gender=current_user.gender_preference)

    # exclude people who were already liked by user
    liked_people = [like.user_to for like in Like.objects.filter(user_from=request.user)]
    people = people.exclude(user__in=liked_people)

    # random shuffle
    people = people.order_by('?')

    return render(request, 'people/users_list.html', {'current_user': current_user,
                                                      'people': people})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.blog_posts.all()
    return render(request, 'people/user_profile.html', {'user': user,
                                                        'posts': posts})


@login_required
@require_POST
def like_user(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'like':
                like = Like.objects.get_or_create(user_from=request.user, user_to=user)[0]
            else:
                Like.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})

        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})


@login_required
def user_activity(request):
    likes_list = Like.objects.filter(Q(user_from=request.user) | Q(user_to=request.user))
    return render(request, 'people/user_activity.html', {'likes_list': likes_list})


@login_required
def find_best_match(request):
    """
    people only with the same relationship type
    Age:
        exact same age = 10 points
        every 1 year of age difference = 10 - difference*2 points
    Gender:
        bisexual = -5 points
    Interests:
        exact same interest = 10 points
        interests from same categories = 5 points
    """
    current_user = request.user.user_info

    # # check if user already used FindMe function during last 24 hours
    if current_user.last_findme_person is not None:
        time_passed = timezone.now() - current_user.last_findme_time

        # if less then 24 hours have passed since last time, show previously found person
        if time_passed.total_seconds() < 60 * 60 * 24:
            best_match = UserProfile.objects.get(user_id=current_user.last_findme_person.id)
            return render(request, 'people/best_match.html', {'person': best_match})

    # evaluation function
    def get_score(person):
        score = 0

        age = person.years_old()
        age_difference = abs(current_user.years_old() - age)
        score += 10 - age_difference

        if person.gender_preference == 'BOTH':
            score -= 5

        user_interests = current_user.interests.all()
        user_interests_groups = [interest.group for interest in user_interests]
        person_interests = person.interests.all()

        for interest in person_interests:
            if interest in user_interests:
                score += 10
            if interest.group in user_interests_groups:
                score += 5

        return score

    # get all profiles
    people = (UserProfile.objects.filter(gender_preference__in=[current_user.gender, 'BOTH'])
              .filter(relationship=current_user.relationship)
              .exclude(user=request.user))

    if current_user.gender_preference != 'BOTH':
        people = people.exclude(gender=current_user.gender)

    liked_people = [like.user_to for like in Like.objects.filter(user_from=request.user)]
    people = people.exclude(user__in=liked_people)

    # score evaluation for every person, sort by score value from highest
    people_scores = {person.user.id: get_score(person) for person in people}
    people_sorted = [person for person, score in sorted(people_scores.items(), key=lambda x: x[1], reverse=True)]

    # save user id with best score and FindMe function time of usage in Cookies
    if current_user.last_findme_person.id != people_sorted[0]:
        best_score_user_id = people_sorted[0]
    else:
        best_score_user_id = people_sorted[1]

    current_user.last_findme_person = User.objects.get(id=best_score_user_id)
    current_user.last_findme_time = timezone.now()
    current_user.save()

    best_match = UserProfile.objects.get(user_id=best_score_user_id)

    return render(request, 'people/best_match.html', {'person': best_match})


@login_required
def report_user(request, reported_user_id):
    reported_user = User.objects.get(id=reported_user_id)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user_from = request.user
            report.reported_user = reported_user
            report.save()
            return redirect(reverse('people:user_detail', kwargs={'username': reported_user.username}))
    else:
        form = ReportForm()
    return render(request, 'people/report_user.html', context={'form': form,
                                                               'reported_user': reported_user})
