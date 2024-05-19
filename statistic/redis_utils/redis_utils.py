import redis
from django.conf import settings
from datetime import date

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


def increment_profile_visits(user_id):
    # Отримання поточної дати
    today = date.today().strftime('%d-%m-%Y')
    print(user_id)
    print(today)
    # Формування ключа для зберігання даних
    # redis_key = f'user:{user_id}:profile_visits:{today}'
    # Збільшення лічильника на 1
    # r.incr(redis_key)


def get_profile_visits(user_id, day):
    # Формування ключа для отримання даних
    redis_key = f'user:{user_id}:profile_visits:{day}'
    # Отримання кількості відвідувань
    return int(r.get(redis_key) or 0)
