from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """  
    This class adds fields from the Recipe model to the admin
    panel
    """

    list_display = (
        'sku',
        'date',
        'name',
        'category',
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
