from django.contrib import admin
from .models import Product, Category, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    This class adds fields from the Recipe model to the admin
    panel
    """

    list_display = (
        'sku',
        'name',
        'category',
        'date',
        'price',
        'image',
    )

    search_fields = ['name', 'category']

    ordering = ('sku',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    This class adds fields from the Review model to the admin
    panel
    """

    list_display = ('name', 'body', 'product', 'created_on',)
    list_filter = ('created_on',)
    search_fields = ['name']
