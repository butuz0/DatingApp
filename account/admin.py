from django.contrib import admin
from .models import UserProfile, Like, GroupOfInterests, Interest


# Register your models here.
@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'gender', 'gender_preference', 'photo']
    raw_id_fields = ['user']


@admin.register(Like)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'created']


@admin.register(GroupOfInterests)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Interest)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'group']
