from django.contrib import messages
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from store.models import Product, Reviews
from store.forms import ReviewForm
from .forms import UserRegistrationForm, UserLoginForm, UserShippingForm, UserDeletionForm
from .models import CustomUser
from order.views import user_orders

from django.db.models import Q
from django_countries import countries


def match(password_1, password_2):
    """
    Used in user_registration function to test if passwords are the same.
    """
    if password_1 == password_2:
        return True
    else:
        return False


def user_registration(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            form.username = form.cleaned_data['username']
            form.email = form.cleaned_data['email']
            form.password_1 = form.cleaned_data['password_1']
            form.password_2 = form.cleaned_data['password_2']
            form.first_name = form.cleaned_data['first_name']
            form.last_name = form.cleaned_data['last_name']
            same_password = match(form.password_1, form.password_2)

            if same_password == True:
                user.set_password(form.password_1)
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('account:user_account_summary')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'account/registration.html', {'form': form})         


@login_required
def user_account_summary(request):
    user = request.user
    return render(request, 'account/account_summary.html', {'user': user})
   

def user_logout(request):
    logout(request)
    return render(request, 'registration/logout.html')


def user_login(request):

    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            form.username = form.cleaned_data['username']
            form.password = form.cleaned_data['password']
            user = authenticate(request, username=form.username, password=form.password)

            if user is not None:
                login(request, user)
                return redirect('account:user_account_summary')

            else:
                messages.error(request, "Username or password is incorrect.")
                return redirect('account:user_login')
    else:
        form = UserLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})


@login_required
def user_details(request, pk):
    user = CustomUser.objects.filter(pk=pk)
    
    if request.method == 'POST':
        form = UserShippingForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save() 
            messages.success(request, 'Account details successfully updated!')
            return redirect('account:user_account_summary')  
    else:
        form = UserShippingForm(instance=request.user)

    return render(request, 'account/details.html', {'form': form, 'user': user, 'countries': countries})        


@login_required
def user_account_deletion(request):

    if request.method == 'POST':

        if request.POST.get('delete'):
            form = UserDeletionForm(request.POST)
            user = CustomUser.objects.get(username=request.user.username)
            user.is_active = False
            user.save()
            return redirect('store:home')

        if request.POST.get('cancel'):
            return redirect('account:user_account_summary')
    else:
        form = UserDeletionForm()
    
    return render(request, 'account/delete_account.html', {'form': form})
 

@login_required
def user_favorite_list(request):
    product_list = Product.products.filter(favorite=request.user.id)
    return render(request, 'account/user_favorites.html', {'product_list': product_list})


@login_required
def user_review_list(request):
    reviews = Reviews.objects.filter(username=request.user.username)
    return render(request, 'account/user_reviews.html', {'reviews': reviews})


@login_required
def user_account_orders(request):
    orders = user_orders(request)
    return render(request, 'account/user_orders.html', {'orders': orders})


@login_required 
def add_to_favorite(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.favorite.filter(id=request.user.id):
        product.favorite.remove(request.user.id)
    else:
        product.favorite.add(request.user.id)
        
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def user_remove_favorite(request, pk):
    product = Product.products.get(pk=pk)
    product.favorite.filter(id=request.user.id)
    product.favorite.remove(request.user.id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def user_remove_review(request, pk):
    username = Q(username=request.user.username)
    product = Q(product=pk)
    review = Reviews.objects.get(username, product)

    if request.method == 'POST':
        review.delete()
        messages.success(request, "Your review has been deleted!")
        return redirect('account:user_account_summary')

    if request.method == 'GET':
        return render(request, 'account/review_update.html')


@login_required   
def user_update_review(request, pk):
    username = Q(username=request.user.username)
    product = Q(product=pk)

    review = Reviews.objects.get(username, product)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review.review = request.POST.get('review')
            review.stars = request.POST.get('stars')
            review.save(update_fields=['review', 'stars'])

            messages.success(request, "Your review has been updated!")
            return redirect('account:user_account_summary')
    else:
        form = ReviewForm()
        
    return render(request, 'account/review_update.html', {'form': form, 'review': review})
