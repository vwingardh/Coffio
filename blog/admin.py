from django.contrib import admin
from .models import Blog, BlogMedia


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']

    prepopulated_fields = {'slug': ('title',),}


@admin.register(BlogMedia)
class Media(admin.ModelAdmin):
    list_display = ['image']
    