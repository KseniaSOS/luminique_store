from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Post, PostCategory
from .forms import PostForm

def all_posts(request):
    """A view to show all posts in Blog"""

    posts = Post.objects.filter(status=1)
    tag = None

    if request.GET:
        if 'tag' in request.GET:
            tag = request.GET['tag'].split(',')
            posts = posts.filter(tag__name__in=tag)
            tag = PostCategory.objects.filter(name__in=tag)

    context = {
        'posts': posts,
        'tag': tag,       
    }

    return render(request, 'posts/all_posts.html', context)


def post_detail(request, slug):
    """A view to show individual post details"""

    post = get_object_or_404(Post, slug=slug)

    context = {
        'post': post,        
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def add_post(request):
    """ Add a post to the blog """

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.slug = slugify(form.instance.title)
            post = form.save()
            messages.success(request, 'The Post is added Successfully!')
            return redirect(
                reverse('post_detail', args=[form.instance.slug]))
        else:
            messages.error(request,
                           'Failed to add post. '
                           'Please ensure the form is valid.')
    else:
        form = PostForm()
    
    template = 'posts/add_post.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
