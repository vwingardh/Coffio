from django.core.exceptions import ObjectDoesNotExist

from .models import Product, Category, Color


def category_filter(filter):
    """
    A function that queries the database using the filter
    chosen by user.
    """
    try:
        category = Category.objects.get(slug=filter)
        products = Product.products.filter(category=category.id)
        if products:
            return products
    except:
        print('category not chosen')
    
    try:
        color = Color.objects.get(color_roast=filter)
        products = Product.products.filter(color_roast=color.id)
        if products:
            return products
    except:
        print('color not chosen')
    
    try:
        products = Product.products.filter(material_features=filter)
        if products:
            return products
    except ObjectDoesNotExist:
        return None
