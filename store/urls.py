from django.urls import path
from . import views


app_name = 'store'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('mission/', views.mission, name='mission'),
    path('faqs/', views.faqs, name='faqs'),
    # email sign up - not user account registration
    path('sign-up/', views.sign_up, name='sign_up'),
    path('search/', views.search_form, name='search_form'),
    path('search/result/', views.search_result, name='search_result'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('store/all-products/', views.all_products, name='all_products'),
    path('store/all-products/<filter>/', views.filter_products, name='filter_products'),
    path('store/<slug:category_slug>/', views.category_list, name='category_list'),
]
