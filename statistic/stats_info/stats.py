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
