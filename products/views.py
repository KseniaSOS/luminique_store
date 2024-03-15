from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile

from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm


def all_products(request):
    """
    A view to show all products,
    including sorting and search queries
    """
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,

    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    A view to show product detailed view.
    """
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.order_by('created_on')    

    if request.method == 'POST':

        if not request.user:
            messages.error(request, 'Sorry, you must login to do that.')
            return redirect(reverse('products'))
        else:
            form = ReviewForm(request.POST, request.FILES,)
            if form.is_valid():
                form.instance.name = request.user.username
                review = form.save(commit=False)
                review.product = product
                review.save()
                messages.success(
                    request,
                    'Successfully posted a review.'
                )
                return redirect(reverse('product_detail', args=[product.id]))

    template = 'products/product_detail.html'
    context = {
        'product': product,
        'reviews': reviews,
        'review_form': ReviewForm(),
    }

    return render(request, template, context)


@login_required
def add_product(request):
    """ Add a product to the store """
    products = Product.objects.all()

    if not request.user.is_superuser:
        messages.error(request, 'You do not have access to this page!')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. '
                           'Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
        'products': products,
        'product': products,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    This view makes it possible to edit a product
    on the site
    """

    products = Product.objects.all()

    if not request.user.is_superuser:
        messages.error(request, 'You do not have access to this page!')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to update product. '
                'Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}.')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
        'products': products,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'You do not have access to this page!')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
