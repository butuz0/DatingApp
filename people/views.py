from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from account.models import UserInfo, Like
import datetime
import requests
import json


def session_expired(request):
    region = request.session.get(settings.USER_REGION_SESSION_ID)
    if not region:
        return True
    return False


def get_user_location():
    key = settings.ABSTRACT_API_KEY
    response = requests.get(f'https://ipgeolocation.abstractapi.com/v1/?api_key={key}')
    return json.loads(response.content.decode())  # user geolocation, decoded from bytes to dictionary


# Create your views here.
@login_required
def list_people(request):
    current_user = request.user.user_info
    if session_expired(request):
        user_location = get_user_location()
        request.session[settings.USER_REGION_SESSION_ID] = f'{user_location["country"]} {user_location["region"]}'
        current_user.latitude = user_location['latitude']
        current_user.longitude = user_location['longitude']
        current_user.save()

    people = UserInfo.objects.filter(preferences__in=['BOTH', current_user.gender]).exclude(user=current_user.user.id)
    if current_user.preferences != 'BOTH':
        people = people.exclude(gender=current_user.gender)

    return render(request, 'people/list.html', {'current_user': current_user,
                                                'people': people})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'people/detail.html', {'user': user})


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
                print(like)
                if like.match():
                    messages.success(request, 'Its a match!')

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
