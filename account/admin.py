from django.contrib import admin
from .models import UserProfile


# Register your models here.
@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'gender', 'gender_preference', 'photo']
    raw_id_fields = ['user']
