from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .redis_utils import get_profile_visits
from .stats_info import get_daily_likes_data, get_relationship_type_data, get_age_groups_data, \
    get_daily_profile_visits_data, get_monthly_likes
from datetime import date, timedelta
import json


# Create your views here.
@login_required
def index(request):
    return render(request, 'statistic/stats.html')


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


@login_required
def get_profile_visits_data(request, days):
    daily_visits = get_daily_profile_visits_data(request.user, days)

    return JsonResponse({
        'daily_visits': daily_visits
    })


@login_required
def profile_visits(request):
    return render(request, 'statistic/profile_visits.html')


@login_required
def monthly_likes(request):
    received, given = get_monthly_likes(request.user)

    return JsonResponse({
        'monthly_likes_received': received,
        'monthly_likes_given': given,
    })
