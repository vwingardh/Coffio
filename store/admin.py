from django.contrib import admin
from .models import (
    Category,
    Reviews,
    Color,
    Media,
    Product,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',),}


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['username', 'review']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['color_roast']


@admin.register(Media)
class Media(admin.ModelAdmin):
    list_display = ['image']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'sku',
        'price',
        'sale_price',
        'color_roast',
        'stock_qty',
        'category',
        'created',
        'updated',
    ]
    prepopulated_fields = {"slug": ("name",),}
