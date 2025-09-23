from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.db.models.functions import Lower

from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm


def all_products(request):
    """
    Display all products, including sorting and search functionality.

    Models Used:
    - Product: Retrieves product list.
    - Category: Retrieves available categories.

    Template Used:
    - products/products.html

    Handles:
    - Sorting products by name, category, rating, or price.
    - Filtering products by search query and category selection.
    """
    products = Product.objects.all()
    query = request.GET.get('q', None)
    categories = request.GET.getlist('category', None)
    sort = request.GET.get('sort', None)
    direction = request.GET.get('direction', None)

    # Sorting Logic
    if sort:
        sort_mapping = {
            'name': 'lower_name',
            'category': 'category__name',
            'rating_asc': 'rating',
            'rating_desc': '-rating',
            'price_asc': 'price',
            'price_desc': '-price',
        }
        sortkey = sort_mapping.get(sort, sort)

        if sortkey == 'lower_name':
            products = products.annotate(lower_name=Lower('name'))

        if direction == 'desc' and not sortkey.startswith('-'):
            sortkey = f'-{sortkey}'

        products = products.order_by(sortkey)

    # Category Filtering
    if categories and categories[0]:  # Only filter if category is not empty
        products = products.filter(category__name__iexact=categories[0])
    elif categories and not categories[0]:
        # Don't filter if category is empty string
        pass

    # Search Filtering
    if query:
        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)
    elif 'q' in request.GET:  # Empty search case
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse('products'))

    all_categories = Category.objects.all()
    current_sorting = f'{sort}_{direction}' if sort and direction else sort

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'all_categories': all_categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    Display a specific product's details.

    Models Used:
    - Product: Fetches the product by ID.

    Template Used:
    - products/product_detail.html
    """
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """
    Allow store owners to add a new product.

    Models Used:
    - Product: Creates a new product entry.

    Form Used:
    - ProductForm: Handles product creation.

    Template Used:
    - products/add_product.html

    Redirects:
    - product_detail: If the product is successfully added.
    - home: If unauthorized access occurs.
    """
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
            messages.error(request, 'Failed to add product.'
                           'Please ensure the form is valid.')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})


@login_required
def edit_product(request, product_id):
    """
    Allow store owners to edit an existing product.

    Models Used:
    - Product: Fetches the product by ID.

    Form Used:
    - ProductForm: Handles product updates.

    Template Used:
    - products/edit_product.html

    Redirects:
    - product_detail: After successful update.
    - home: If unauthorized access occurs.
    """
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
            messages.error(request, 'Failed to update product.'
                           'Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    return render(request, 'products/edit_product.html',
                  {'form': form, 'product': product})


@login_required
def delete_product(request, product_id):
    """
    Allow store owners to delete a product.

    Models Used:
    - Product: Fetches the product by ID.

    Redirects:
    - products: After successful deletion.
    - home: If unauthorized access occurs.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    # Remove reference from related order line items
    related_items = product.orderlineitem_set.all()
    for item in related_items:
        item.product = None
        item.save()

    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


@login_required
def add_review(request, product_id):
    """
    Allow logged-in users to submit a review for a product.

    Models Used:
    - Product: Fetches the product by ID.
    - Review: Creates a new review.

    Redirects:
    - product_detail: After successful submission.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        # ✅ Ensure rating is not None and is a valid number
        try:
            rating = int(rating)
        except (TypeError, ValueError):
            messages.error(request, "Invalid rating."
                           " Please select a valid rating.")
            return redirect('product_detail', product_id=product.id)

        # ✅ Check if rating is within range
        if not (1 <= rating <= 5):
            messages.error(request, "Invalid rating. Must be between 1 and 5.")
            return redirect('product_detail', product_id=product.id)

        # ✅ Ensure comment is not empty
        if not comment:
            messages.error(request, "Please provide"
                           "a comment for your review.")
            return redirect('product_detail', product_id=product.id)

        # ✅ Create the review
        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

        # ✅ Update product rating if applicable
        if hasattr(product, 'update_rating'):
            product.update_rating()

        messages.success(request, "Review submitted successfully!")
        return redirect('product_detail', product_id=product.id)

    return redirect('product_detail', product_id=product.id)



@login_required
def edit_review(request, review_id):
    """
    Allow users to edit their existing review.

    Models Used:
    - Review: Fetches the review by ID.

    Form Used:
    - ReviewForm: Handles review updates.

    Template Used:
    - products/edit_review.html

    Redirects:
    - profile: After successful edit.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)

    # ✅ Always initialize the form with the review instance
    form = ReviewForm(instance=review)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, 'products/edit_review.html',
                  {'form': form, 'review': review})



@login_required
def delete_review(request, review_id):
    """
    Allow users to delete their review.

    Models Used:
    - Review: Fetches the review by ID.

    Redirects:
    - profile: After successful deletion.
    """
    review = get_object_or_404(Review, id=review_id)

    if request.method == "POST":
        if request.user == review.user or request.user.is_superuser:
            review.delete()
            messages.success(request, "Review deleted successfully!")
        else:
            messages.error(request, "You do not have permission"
                           "to delete this review.")

    return redirect("profile")
