from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .redis_utils import increment_profile_visits, get_profile_visits
from .stats_info import get_daily_likes_data, get_relationship_type_data
from datetime import date, timedelta
import json


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


@login_required
def get_profile_likes_data(request, days):
    received, given = get_daily_likes_data(request.user, days)

    return JsonResponse({
        'daily_likes_received': received,
        'daily_likes_given': given
    })


@login_required
def profile_likes(request):
    return render(request, 'statistic/profile_likes.html')


@login_required
def relationship_types_analysis(request):
    received, given = get_relationship_type_data(request.user)

    context = {
        'relationship_data_received': json.dumps(received),
        'relationship_data_given': json.dumps(given),
    }

    return render(request, 'statistic/relationship_analysis.html', context)


@login_required
def age_analysis(request):
    received, given = get_age_groups_data(request.user)

    context = {
        'received_age_data': json.dumps(received),
        'given_age_data': json.dumps(given),
    }

    return render(request, 'statistic/age_analysis.html', context)
