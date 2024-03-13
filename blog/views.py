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


@login_required
def edit_post(request, slug):
    """Edit a posts in the blog"""

    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(
            request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.slug = slugify(form.instance.title)
            form.save()
            messages.success(
                request, f'The Post - {post.title} is updated successfully!')
            return redirect(reverse('post_detail', args=[post.slug]))
        else:
            messages.error(request, 'Failed to update blog post. '
                           'Please ensure the form is valid.')
    else:
        form = PostForm(instance=post)
        messages.info(request, f'You are editing {post.title}.')

    template = 'posts/edit_post.html'
    context = {
        'form': form,
        'post': post,
    }
    return render(request, template, context)


@login_required
def delete_post(request, slug):
    """ This view deletes apost from the blog """

    if not request.user.is_superuser:
        messages.error(request, 'You do not have access to this page!')
        return redirect(reverse('home'))

    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, 'Successfully deleted post!')
    return redirect(reverse('posts'))
