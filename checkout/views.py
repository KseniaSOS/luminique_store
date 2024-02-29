from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your shopping bag is still empty")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51OpFksEX9mgoi5oacnQxXmCWlo33G4YStFPIWvT4swncyaFaIN8qOWQ9xkWW6cSng50WBCKAM8KRlJdAKckXUUDH00Je7eibHN',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)