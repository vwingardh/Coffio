from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('registration/', views.user_registration, name='user_registration'),
    path('summary/', views.user_account_summary, name='user_account_summary'),
    path('summary/details/<int:pk>/', views.user_details, name='user_details'),
    path('summary/deletion/', views.user_account_deletion, name='user_account_deletion'),
    path('reviews/', views.user_review_list, name='user_review_list'),
    path('summary/reviews/<int:pk>/', views.user_remove_review, name='user_remove_review'),
    path('summary/reviews/<int:pk>/update/', views.user_update_review, name='user_update_review'),
    path('summary/orders/', views.user_account_orders, name='user_account_orders'),
    path('summary/favorites/', views.user_favorite_list, name='user_favorite_list'),
    path('summary/favorite/<int:pk>/', views.add_to_favorite, name='add_to_favorite'),
    path('summary/favorites/<int:pk>/remove/', views.user_remove_favorite, name='user_remove_favorite'),
]
