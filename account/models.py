from django.db import models
from django.conf import settings
from django.urls import reverse
import datetime


# Create your models here.
class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male',
        FEMALE = 'F', 'Female'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=Gender.choices, null=True)
    date_of_birth = models.DateField(null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', null=True)
    pref_choice = Gender.choices + [('BOTH', 'Male and Female')]
    preferences = models.CharField(max_length=4, choices=pref_choice, null=True)
    about_me = models.TextField(null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

    def get_absolute_url(self):
        return reverse('people:user_detail', args=[self.user.username])

    def years_old(self):
        return datetime.date.today().year - self.date_of_birth.year
