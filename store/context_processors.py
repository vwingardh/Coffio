from .models import Category, Color


def categories(request):
    return {'categories': Category.objects.all()}


def color_or_roast(request):
    return {'color_or_roast': Color.objects.all()}
