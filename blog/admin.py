from django.contrib import admin
from .models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'updated', 'text', 'author']
    list_filter = ['created', 'publish', 'author']
    search_fields = ['text']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['publish']
