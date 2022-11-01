from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('blog-list/', views.blog_list, name='blog_list'),
    path('blog-list/<slug:slug>/', views.blog_article, name='blog_article'),
    path('blog-list/favorite/<int:pk>/', views.blog_favorite, name='blog_favorite'),
    path('blog-favorites/', views.blog_favorites_list, name='blog_favorites_list'),
    path('blog-favorites/remove/<int:pk>/', views.blog_remove_favorite, name='blog_remove_favorite'),
]
