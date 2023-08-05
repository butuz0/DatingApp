from django.db import models
from django.conf import settings
import datetime


# Create your models here.
class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male',
        FEMALE = 'F', 'Female'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=Gender.choices, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True)
    pref_choice = Gender.choices + [('BOTH', 'Male and Female')]
    preferences = models.CharField(max_length=4, choices=pref_choice, null=True,
                                   blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
