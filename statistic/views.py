from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from people.views import Like
from .redis_utils import increment_profile_visits, get_profile_visits
from datetime import date, timedelta


# Create your views here.
@login_required
def index(request):
    return render(request, 'statistic/stats.html')


@login_required
def profile_visits(request, days):
    today = date.today()
    start_date = today - timedelta(days=days)

    visits = {}
    for n in range((today - start_date).days + 1):
        day = start_date + timedelta(days=n)
        visits[day] = get_profile_visits(request.user, day.strftime('%d-%m-%Y'))

    return render(request, 'statistic/profile_visits.html', {
        'visits': visits})


def get_likes(user, days):
    today = date.today() + timedelta(days=1)
    start_date = today - timedelta(days=days)

    likes_received = Like.objects.filter(user_to=user, created__range=[start_date, today])
    likes_given = Like.objects.filter(user_from=user, created__range=[start_date, today])

    return likes_received, likes_given


@login_required
def get_profile_likes_data(request, days):
    likes_received, likes_given = get_likes(request.user, days)

    today = date.today() + timedelta(days=1)
    start_date = today - timedelta(days=days)

    daily_likes_received = {}
    daily_likes_given = {}
    for n in range((today - start_date).days + 1):
        day = start_date + timedelta(days=n)
        next_day = day + timedelta(days=1)

        day_likes_received = likes_received.filter(created__gte=day, created__lt=next_day).count()
        day_likes_given = likes_given.filter(created__gte=day, created__lt=next_day).count()

        daily_likes_received[day.strftime('%d-%m')] = day_likes_received
        daily_likes_given[day.strftime('%d-%m')] = day_likes_given

    return JsonResponse({
        'daily_likes_received': daily_likes_received,
        'daily_likes_given': daily_likes_given
    })


@login_required
def profile_likes(request):
    return render(request, 'statistic/profile_likes.html')
