from django.shortcuts import render, request
from .models import Post

def all_posts(request):
    """A view to show all posts in Blog"""

    posts = Post.objects.filter(status=1)

    context = {
        'posts': posts,        
    }

    return render(request, 'posts/all_posts.html', context)