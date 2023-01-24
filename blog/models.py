from django.db import models
from account.models import CustomUser
from django.urls import reverse


class BlogMedia(models.Model):
    """
    Creates media for blog posts.
    """
    image = models.ImageField(upload_to='blog/')
    is_default = models.BooleanField(default=True)

    class Meta: 
        verbose_name = "blog image"
        verbose_name_plural = "blog images"
    
    def __str__(self):
        return self.image.url


class BlogManager(models.Manager):
    """
    Manager returns only blog posts that have been set to publish.
    """
    def get_queryset(self):
        return super(BlogManager, self).get_queryset().filter(status=1)


# Choices for Blog model
STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Blog(models.Model):
    """
    Creates Blog posts created by admin users.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    image = models.ForeignKey(BlogMedia, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(CustomUser, related_name="user_favorites", blank=True)
    blogs = BlogManager() 

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse("blog:blog_article", args=[self.slug])

    def get_favorites(slug):
        """
        Returns integer for number of users who have favorited a blog post
        based on blog post slug.
        """
        favorites = Blog.blogs.get(slug=slug)
        return favorites.favorite.count()

    def __str__(self):
        return self.title
