from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order
from products.models import Product


@login_required
def profile(request):
    """ Display the user's profile. """

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    """This view displays the order history
    on a checkout success page"""

    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
            f'This is a past confirmation for order number {order_number}. '
            'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,        
    }

    return render(request, template, context)


@login_required
def wishlist(request):
    """Users wishlist"""

    products = Product.objects.filter(users_wishlist=request.user)
    template = 'profiles/wishlist.html'
    context = {
        'products': products,
    }

    return render(request, template, context)

@login_required
def add_to_wishlist(request, id):
    """Add product to the wishlist"""

    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(
            request, 'Removed ' + product.name + ' from your wishlist')
        return redirect(reverse('wishlist'))

    else:
        product.users_wishlist.add(request.user)
        messages.success(
            request, 'Added ' + product.name + ' to your wishlist')

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
