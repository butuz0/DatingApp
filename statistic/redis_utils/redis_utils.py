import redis
from django.conf import settings
from datetime import date

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


# add users who visited profile to database
def add_profile_visits(user_id, visitor_id):
    if user_id == visitor_id:
        return
    today = date.today().strftime('%d-%m-%Y')
    redis_key = f'user:{user_id}:profile_visits:{today}'
    r.sadd(redis_key, str(visitor_id))


def get_profile_visits(user_id, day):
    day_formatted = day.strftime('%d-%m-%Y')
    redis_key = f'user:{user_id}:profile_visits:{day_formatted}'
    return r.scard(redis_key)
