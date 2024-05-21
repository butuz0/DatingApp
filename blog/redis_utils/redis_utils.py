import redis
from django.conf import settings

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


# adds persons like to comment
def add_comment_like(user_id, comment_id):
    r.sadd(f'comment:{comment_id}:likes', user_id)


# removes persons like from comment
def remove_comment_like(user_id, comment_id):
    r.srem(f'comment:{comment_id}:likes', user_id)


# returns total comments likes
def get_comment_likes_count(comment_id):
    return r.scard(f'comment:{comment_id}:likes')


# checks if person has liked the comment
def has_liked_comment(user_id, comment_id):
    return r.sismember(f'comment:{comment_id}:likes', user_id)


# adds persons like to post
def add_post_like(user_id, post_id):
    r.sadd(f'post:{post_id}:likes', user_id)


# removes persons like from post
def remove_post_like(user_id, post_id):
    r.srem(f'post:{post_id}:likes', user_id)


# returns total post likes
def get_post_likes_count(post_id):
    return r.scard(f'post:{post_id}:likes')


# checks if person has liked the post
def has_liked_post(user_id, post_id):
    return r.sismember(f'post:{post_id}:likes', user_id)
