from django.contrib import admin
from .models import BlogPost, UserProfile

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'view_count', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('category', 'created_at', 'author')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
