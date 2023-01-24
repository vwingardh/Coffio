from django.db import models
from django.urls import reverse
from django.conf import settings
from account.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta: 
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class Color(models.Model):
    color_roast = models.CharField(
        max_length=150, 
        help_text='Please enter coffee cup color or coffee bean roast.'
    )

    class Meta:
        verbose_name_plural = "Color variants"

    def __str__(self):
        return self.color_roast


class Media(models.Model):
    image = models.ImageField(upload_to='images/')
    product_association = models.CharField(max_length=150, blank=False)
    is_default = models.BooleanField(default=True)

    class Meta: 
        verbose_name = "product image"
        verbose_name_plural = "product images"
    
    def get_product_images(product_association):
        """
        A function that returns all images based on the product's assigned
        association, such as color or blend.
        """
        product_images = Media.objects.filter(product_association=product_association)
        return product_images
        
    def __str__(self):
        return self.image.url


class ProductManager(models.Manager):
    """
    Product manager returns all products that have been set to is_active = True.
    """
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


# Choices for the material_features field in the Product model
PRODUCT_MATERIAL_FEATURES = (
    ('tempered glass', 'tempered glass'),
    ('colombian blend', 'colombian blend'),
    ('peruvian blend', 'peruvian blend'),
    ('costa rica blend', 'costa rica blend')
)


class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    sku = models.IntegerField(db_index=True, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    sale_price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ForeignKey(
        Media, 
        help_text='Upload a product image', 
        on_delete=models.CASCADE
    )
    color_roast = models.ForeignKey(Color, on_delete=models.CASCADE)
    material_features = models.CharField(
        choices=PRODUCT_MATERIAL_FEATURES, 
        max_length=25
    )
    height = models.IntegerField(blank=True, null=True)
    volume = models.IntegerField(blank=True)
    stock_qty = models.IntegerField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='product_creator', 
        on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=255)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    favorite = models.ManyToManyField(
        CustomUser, 
        related_name="favorites", 
        blank=True
    ) 
    products = ProductManager()

    class Meta: 
        verbose_name_plural = "Products"
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def total_favorites(slug):
        item = Product.products.get(slug=slug)
        return item.favorite.count()
  
    def __str__(self):
        return self.name


class Reviews(models.Model):
    # choices for stars field
    RATINGS = [
        (5, 5), 
        (4, 4), 
        (3, 3),
        (2, 2),
        (1, 1)
    ]
    user = models.ManyToManyField(CustomUser)
    username = models.TextField(blank=True)
    review = models.TextField(max_length=2000, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    stars = models.IntegerField(
        choices=RATINGS,
        default=5,
        blank=True
    )
    verified = models.BooleanField(default=True)

    class Meta: 
        verbose_name = "User review"
        verbose_name_plural = "User reviews"

    def get_average_rating(pk):
        """
        A function for returning the average star rating
        based on an individual product.
        """
        reviews = Reviews.objects.filter(product=pk).values('stars')
        if reviews:
            sum = 0
            count = 0

            for stars in reviews:
                star = stars.get('stars')
                sum = sum + int(star)
                count += 1
            
            avg = sum / count
            return avg 
        else:
            return None

    def match(request, current_product_id):
        """
        A function that creates a list of users who have reviewed current product. 
        Function checks if current user has left a review, prevents multiple
        reviews being made by one user.
        """
        queryset = Reviews.objects.filter(product=current_product_id).values('username')
        review_usernames = []

        if queryset:
            for i in queryset:
                queryset_username = i.get('username')
                review_usernames.append(queryset_username)
        else:
            return False
        if request.user.username in review_usernames:
            return True
        else: 
            return False

    def __str__(self):
        return self.review


class EmailList(models.Model):
    """
    A model for collecting sign up emails.
    """
    email = models.EmailField(blank=True)
