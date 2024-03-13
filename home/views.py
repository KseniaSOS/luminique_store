from django.shortcuts import render


def privacy_policy(request):
    """
    This view renders the privacy page
    """
    return render(request, 'home/privacy_policy.html')


def index(request):
    """A view to return the index page"""

    return render(request, 'home/index.html')
