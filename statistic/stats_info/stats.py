from django.db.models import Count
from datetime import date, timedelta
from account.models import Like


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
