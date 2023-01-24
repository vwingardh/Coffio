from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from .models import Product, Media, Reviews, Category
from .forms import ReviewForm, EmailListForm
from store.product_filters import category_filter


class ProductListView(generic.ListView):
    model = Product
    context_object_name = 'product_list'
    queryset = Product.products.all().order_by('-name')[0:4]
    template_name = 'store/home.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['reviews'] = Reviews.objects.all()[0:4]
        return context


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    images = Media.get_product_images(product.image.product_association)
    favorites = Product.total_favorites(slug)
    average = Reviews.get_average_rating(pk=product.id)
    reviews = Reviews.objects.filter(product=product.id)  
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            previous_review = Reviews.match(request, product.id)
            if previous_review == True:
                messages.error(request, 'This username has already created a review for this product.')
                return redirect(reverse('store:product_detail', kwargs={'slug': slug}))
            else:
                review = form.save(commit=False)
                review.product = product
                review.save()
                messages.success(request, "Your review has been submitted!")
                return redirect(reverse('store:product_detail', kwargs={'slug': slug}))
    else:
        form = ReviewForm()
    return render(request, 'products/single_product.html', {
        'product': product, 
        'images': images, 
        'form': form, 
        'average': average, 
        'favorites': favorites,
        'reviews': reviews
    })


def all_products(request):
    products = Product.products.all()
    return render(request, 'products/all_products.html', {'products': products})


def filter_products(request, filter):
    products = category_filter(filter)
    if products:
        return render(request, 'products/all_products.html', {'products': products})
    else:
        messages.error(request, 'No items where found.')
        return render(request, 'products/all_products.html')


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.products.filter(category=category)
    return render(request, 'products/category_list.html', {'category': category, 'products': products})


# Email sign up list - not user account registration       
def sign_up(request):
    if request.method == 'POST':
        form = EmailListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = EmailListForm()
    return render(request, 'account/account_summary.html', {'form': form})


def search_form(request):
    return render(request, 'store/search_form.html')


def search_result(request):
    if request.method == 'POST':
        search_input = request.POST['search_input']
        if search_input:
            search_results = Product.products.filter(name__contains=search_input)
            return render(request, 'store/search_result.html', {
                'search_input': search_input, 
                'search_results': search_results
            })
        else:
            messages.error(request, "Sorry, there are no results for that search.")
            return render(request, 'store/search_result.html')
    else:
        return render(request, 'store/search_result.html')
        

def mission(request):
    return render(request, 'store/resources/mission.html')


def faqs(request):
    return render(request, 'store/resources/faqs.html')
    