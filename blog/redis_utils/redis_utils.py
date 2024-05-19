import redis
from django.conf import settings

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


# adds persons like to comment
def add_like(user_id, comment_id):
    r.sadd(f'comment:{comment_id}:likes', user_id)


# removes persons like from comment
def remove_like(user_id, comment_id):
    r.srem(f'comment:{comment_id}:likes', user_id)


# returns total comments likes
def get_likes_count(comment_id):
    return r.scard(f'comment:{comment_id}:likes')


# checks if person has liked the comment
def has_liked(user_id, comment_id):
    return r.sismember(f'comment:{comment_id}:likes', user_id)
