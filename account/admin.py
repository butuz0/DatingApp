from django.contrib import admin
from .models import UserInfo


# Register your models here.
@admin.register(UserInfo)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'gender', 'preferences', 'photo']
    raw_id_fields = ['user']
