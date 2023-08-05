from django.db import models
from django.conf import settings


# Create your models here.
class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male',
        FEMALE = 'F', 'Female'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=Gender.choices)
    date_of_birth = models.DateTimeField()
    photo = models.ImageField(upload_to='users/%Y/%m/%d/')
    preferences = models.CharField(max_length=4, choices=Gender.choices.append(('Male and Female', 'BOTH')))

    def __str__(self):
        return f'Profile of {self.user.username}'
