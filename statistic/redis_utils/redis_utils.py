import redis
from django.conf import settings
from datetime import date

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


# increment today`s users profile visits by one
def increment_profile_visits(user_id):
    today = date.today().strftime('%d-%m-%Y')
    redis_key = f'user:{user_id}:profile_visits:{today}'
    r.incr(redis_key)


def get_profile_visits(user_id, day):
    redis_key = f'user:{user_id}:profile_visits:{day}'
    return int(r.get(redis_key) or 0)
