from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog.models import Blog


def blog_list(request):
    blog_list = Blog.blogs.all()
    return render(request, 'blog/blog.html', {'blog_list': blog_list})


def blog_article(request, slug):
    article = get_object_or_404(Blog, slug=slug, status=1)
    favorites = Blog.get_favorites(slug)
    return render(request, 'blog/article.html', {'article': article, 'favorites': favorites})


@login_required 
def blog_favorite(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.favorite.filter(id=request.user.id):
        blog.favorite.remove(request.user.id)
    else:
        blog.favorite.add(request.user.id)  
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def blog_favorites_list(request):
    blog_list = Blog.blogs.filter(favorite=request.user)
    return render(request, 'account/user_blog_favorites.html', {'blog_list': blog_list})


@login_required
def blog_remove_favorite(request, pk):
    blog = Blog.blogs.get(pk=pk)
    blog.favorite.filter(id=request.user.id)
    blog.favorite.remove(request.user.id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
