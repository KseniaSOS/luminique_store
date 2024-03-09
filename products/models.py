from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """ Category Model """
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=250)
    view_name = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_view_name(self):
        return self.view_name  


class Product(models.Model):
    """ Product model that provides all products that are on sale """

    class Meta:
        """
        This meta class orders the model by date.
        """
        ordering = ['-date']

    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, null=True)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)    
    price = models.DecimalField(max_digits=6, decimal_places=2)  
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)
    sku = models.CharField(max_length=254, null=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)    
    image = models.ImageField(null=True, blank=True)
    users_wishlist = models.ManyToManyField(User)
    on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Model acting as reviews linked to each Product
    """
    class Meta:
        verbose_name_plural = "Reviews"
        ordering = ['created_on']

    product = models.ForeignKey(
         Product, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=50)    
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.body} by {self.name}"