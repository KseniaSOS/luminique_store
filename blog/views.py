from django.shortcuts import render, get_object_or_404


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



def add_post(request):
    """ Add a post to the blog """
    form = PostForm()
    template = 'posts/add_post.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
