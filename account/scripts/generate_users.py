from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.contrib.auth.models import User
from account.models import UserProfile, Interest, Like
from randomuser import RandomUser
from random import randint, choice, choices
import requests


def generate_users(num_users):
    random_users = RandomUser.generate_users(num_users)
    for random_user in random_users:
        # generate User object
        user = User.objects.create_user(username=random_user.get_username(),
                                        email=random_user.get_email(),
                                        password=random_user.get_password(),
                                        first_name=random_user.get_first_name(),
                                        last_name=random_user.get_last_name())
        user.save()

        # for generated User generate User Profile
        user_profile = UserProfile.objects.create(user=user,
                                                  gender=random_user.get_gender()[0].capitalize(),
                                                  date_of_birth=random_user.get_dob()[:10],
                                                  gender_preference=choice(UserProfile.pref_choice)[0],
                                                  relationship=choice(UserProfile.Relationship.choices)[0])

        # choose random interests
        interests_amount = randint(5, 10)
        interests = choices(Interest.objects.all(), k=interests_amount)
        user_profile.interests.set(interests)
        response = requests.get(random_user.get_picture('large'))

        # add photo
        if response.status_code == 200:
            pic_temp = NamedTemporaryFile()
            pic_temp.write(response.content)
            pic_temp.flush()
            user_profile.photo.save(f'{user.username}.jpg', File(pic_temp))

        user_profile.save()

        # generate Likes
        all_users = (UserProfile.objects
                     .filter(gender_preference__in=['BOTH', user_profile.gender])
                     .exclude(user=user.id))
        try:
            likes_amount = randint(1, len(all_users))
            users_liked = set()
            users_liked.update(choices(all_users, k=likes_amount))
        except ValueError or IndexError:
            continue
        else:
            for liked_user in users_liked:
                like, created = Like.objects.get_or_create(user_from=user, user_to=liked_user.user)
