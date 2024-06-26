from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
import datetime


class GroupOfInterests(models.Model):
    name = models.CharField(max_length=50)
    background_color = models.CharField(max_length=10, default='#FFFFFF')

    def __str__(self):
        return f'{self.name} : {self.background_color}'


class Interest(models.Model):
    name = models.CharField(max_length=50)
    group = models.ForeignKey(GroupOfInterests, related_name='interests', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Create your models here.
class UserProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male',
        FEMALE = 'F', 'Female',
        BOTH = 'BOTH', 'Male and Female'

    class Relationship(models.TextChoices):
        SHORT = 'short', 'Short Relationship',
        LOVE = 'love', 'True Love',
        FRIEND = 'friend', 'Friendship',
        FUN = 'fun', 'Having Fun'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_info', on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=Gender.choices[:-1], null=True)
    date_of_birth = models.DateField(null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', null=True)
    gender_preference = models.CharField(max_length=4, choices=Gender.choices, null=True)
    about_me = models.TextField(null=True, max_length=250)
    relationship = models.CharField(max_length=6, choices=Relationship.choices, null=True)
    interests = models.ManyToManyField(Interest)
    last_findme_person = models.ForeignKey('auth.User', related_name='last_findme_person', null=True,
                                           on_delete=models.SET_NULL)
    last_findme_time = models.DateTimeField(null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

    def get_absolute_url(self):
        return reverse('people:user_detail', args=[self.user.username])

    def years_old(self):
        return datetime.date.today().year - self.date_of_birth.year


class Like(models.Model):
    user_from = models.ForeignKey('auth.User', related_name='like_user_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='like_user_to', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ['-created']

    # check if two users like each other
    def match(self):
        return Like.objects.filter(user_to=self.user_from, user_from=self.user_to).exists()

    def __str__(self):
        return f'{self.user_from} liked {self.user_to} at {self.created}'


user_model = get_user_model()
user_model.add_to_class('likes', models.ManyToManyField('self',
                                                        through=Like,
                                                        related_name='liked_by',
                                                        symmetrical=False))


class Report(models.Model):
    class ViolationType(models.TextChoices):
        SPAM = 'spam', 'Spam',
        FAKE = 'fake', 'Fake Profile',
        HARASS = 'harass', 'Harassment',
        HATE = 'hate', 'Hate Speech',
        SCAM = 'scam', 'Scam',
        PICTURE = 'picture', 'Inappropriate Picture',
        UNDERAGE = 'underage', 'Underage User',
        STALKING = 'stalking', 'Stalking',
        PROFILE = 'profile', 'Inappropriate Profile'

    user_from = models.ForeignKey('auth.User', related_name='user_from', on_delete=models.CASCADE)
    reported_user = models.ForeignKey('auth.User', related_name='reported_user', on_delete=models.CASCADE)
    report_reason = models.CharField(max_length=10, choices=ViolationType.choices, null=True)
    description = models.TextField(max_length=250, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} reported {self.reported_user} on {self.created}'
