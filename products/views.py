from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.db.models.functions import Lower

from .models import Product, Category,  Review
from .forms import ProductForm, ReviewForm

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            
            # Custom sorting mapping
            sort_mapping = {
                'name': 'lower_name',
                'category': 'category__name',
                'rating_asc': 'rating',
                'rating_desc': '-rating',
                'price_asc': 'price',
                'price_desc': '-price',
            }

            if sortkey in sort_mapping:
                sortkey = sort_mapping[sortkey]

                # Special case: sorting by name requires annotation
                if sortkey == 'lower_name':
                    products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc' and not sortkey.startswith('-'):
                    sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            print(f"Categories from request: {categories}")
            matching_categories = Category.objects.filter(name__iexact=categories[0])  # Case-insensitive match
            print(f"Matching Categories in DB: {matching_categories}")
            products = products.filter(category__name__iexact=categories[0])
            print(f"Filtered Products: {products}")

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # Always include all categories in the context
    all_categories = Category.objects.all()
    current_sorting = f'{sort}_{direction}' if sort and direction else sort

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'all_categories': all_categories,  # Add all categories here
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    # Update related order line items
    related_items = product.orderlineitem_set.all()  # Adjust based on your related name
    for item in related_items:
        item.product = None
        item.save()

    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))

# leave a review
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")
        
        if not (1 <= rating <= 5):
            messages.error(request, "Invalid rating. Must be between 1 and 5.")
            return redirect('product_detail', product_id=product.id)
        
        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )
        product.update_rating()
        messages.success(request, "Review submitted successfully!")
        return redirect('product_detail', product_id=product.id)

    return redirect('product_detail', product_id=product.id)

# edit a review
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = ReviewForm(instance=review)

    return render(request, 'products/edit_review.html', {'form': form})

# delete a review
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == "POST":
        if request.user == review.user or request.user.is_superuser:
            review.delete()
            messages.success(request, "Review deleted successfully!")
        else:
            messages.error(request, "You do not have permission to delete this review.")
    
    return redirect("profile")