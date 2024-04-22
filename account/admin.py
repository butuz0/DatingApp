from django.contrib import admin
from .models import UserProfile, Like, GroupOfInterests, Interest, Report


# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'gender', 'gender_preference', 'photo']
    raw_id_fields = ['user']
    search_fields = ['user__username']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'created']


@admin.register(GroupOfInterests)
class GroupOfInterestsAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ['name', 'group']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'reported_user', 'created']
