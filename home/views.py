from django.shortcuts import render


def faq(request):
    """
    This view renders the faq page
    """
    return render(request, 'home/faq.html')


def privacy_policy(request):
    """
    This view renders the privacy policy page
    """
    return render(request, 'home/privacy_policy.html')


def index(request):
    """A view to return the index page"""

    return render(request, 'home/index.html')
