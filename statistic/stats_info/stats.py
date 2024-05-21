from django.db.models import Count
from django.db.models.functions import TruncMonth
from account.models import Like, UserProfile
from ..redis_utils import get_profile_visits
from datetime import date, timedelta
from collections import defaultdict


def get_likes(user, days: int = None):
    if days is not None:
        today = date.today() + timedelta(days=1)
        start_date = today - timedelta(days=days)

        likes_received = Like.objects.filter(user_to=user, created__range=[start_date, today])
        likes_given = Like.objects.filter(user_from=user, created__range=[start_date, today])
    else:
        likes_received = Like.objects.filter(user_to=user)
        likes_given = Like.objects.filter(user_from=user)

    return likes_received, likes_given


def get_daily_likes_data(user, days):
    likes_received, likes_given = get_likes(user, days)

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

    return daily_likes_received, daily_likes_given


def get_relationship_type_data(user):
    received_likes, given_likes = get_likes(user)

    received_relationship_data = (received_likes
                                  .values('user_from__user_info__relationship')
                                  .annotate(count=Count('id')))

    given_relationship_data = (given_likes
                               .values('user_to__user_info__relationship')
                               .annotate(count=Count('id')))

    received_relationship_data_dict = {item['user_from__user_info__relationship']: item['count']
                                       for item in received_relationship_data}
    given_relationship_data_dict = {item['user_to__user_info__relationship']: item['count']
                                    for item in given_relationship_data}

    return received_relationship_data_dict, given_relationship_data_dict


def age_group(age):
    if age < 25:
        return '18-24'
    elif age < 35:
        return '25-34'
    elif age < 45:
        return '35-44'
    elif age < 55:
        return '45-54'
    elif age < 65:
        return '55-64'
    else:
        return '65+'


def get_age_groups_data(user):
    received_likes, given_likes = get_likes(user)

    received_ages = [UserProfile.objects.get(user_id=like.user_from.id).years_old() for like in received_likes]
    given_ages = [UserProfile.objects.get(user_id=like.user_to.id).years_old() for like in given_likes]

    received_age_counts = defaultdict(int)
    given_age_counts = defaultdict(int)

    for age in received_ages:
        received_age_counts[age_group(age)] += 1

    for age in given_ages:
        given_age_counts[age_group(age)] += 1

    return received_age_counts, given_age_counts


def get_daily_profile_visits_data(user, days):
    today = date.today()
    start_date = today - timedelta(days=days)

    daily_visits = {}
    for n in range((today - start_date).days + 1):
        day = start_date + timedelta(days=n)
        daily_visits[day.strftime('%d-%m')] = get_profile_visits(user, day)

    return daily_visits


def get_monthly_likes(user):
    today = date.today()

    # Генеруємо список останніх 6 місяців
    months = []
    for i in range(6, -1, -1):
        month = today.replace(day=1) - timedelta(days=i * 30)
        months.append(month)

    received_likes = (Like.objects.filter(user_to=user, created__gte=months[0])
                      .annotate(month=TruncMonth('created'))
                      .values('month')
                      .annotate(like_count=Count('id'))
                      .order_by('month'))

    given_likes = (Like.objects.filter(user_from=user, created__gte=months[0])
                   .annotate(month=TruncMonth('created'))
                   .values('month')
                   .annotate(like_count=Count('id'))
                   .order_by('month'))

    received_likes_dict = {like['month'].strftime('%B'): like['like_count'] for like in received_likes}
    given_likes_dict = {like['month'].strftime('%B'): like['like_count'] for like in given_likes}

    monthly_received_likes = {month.strftime('%B'): received_likes_dict.get(month.strftime('%B'), 0) for month in
                              months}
    monthly_given_likes = {month.strftime('%B'): given_likes_dict.get(month.strftime('%B'), 0) for month in
                           months}

    return monthly_received_likes, monthly_given_likes
