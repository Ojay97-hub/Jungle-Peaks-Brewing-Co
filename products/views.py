from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.
def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    categories = Category.objects.all()  # Ensure categories are included
    query = None
    current_categories = None
    sort = None

    if request.GET:
        if 'category' in request.GET:
            current_categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=current_categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

        if 'sort' in request.GET:
            sort = request.GET['sort']
            if sort == 'price':
                products = products.order_by('price')
            elif sort == 'rating':
                products = products.order_by('-rating')

        if sort:
            if sort == 'price_asc':
                products = products.order_by('price')
            elif sort == 'price_desc':
                products = products.order_by('-price')
            elif sort == 'rating_asc':
                products = products.order_by('rating')
            elif sort == 'rating_desc':
                products = products.order_by('-rating')

    context = {
        'products': products,
        'categories': categories,  # Pass categories to the template
        'search_term': query,
        'current_categories': current_categories,
        'current_sort': sort,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

