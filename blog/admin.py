from django.contrib import admin
from .models import Blog, BlogCategory


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    """
    Adds fields to the admin area 
    """

    list_display = ('name', )
    list_filter = ('name', )



@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'excerpt', 'tag', 'created_on',
                    'author', 'featured_image', 'status',)
    search_fields = ['title', 'tag']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    actions = ['publish', 'unpublish']

    def publish(self, request, queryset):
        """
        This help method updates the status field to 1
        """

        queryset.update(status=1)

    def unpublish(self, request, queryset):
        """
        This help method updates the status field to 0
        """

        queryset.update(status=0)

