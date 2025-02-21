from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages

from products.models import Product


def view_bag(request):
    """
    Display the shopping bag page.

    Template Used:
    - bag/bag.html
    """
    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """
    Add a specified quantity of a product to the shopping bag.

    Request Type:
    - POST: Adds the product to the session cart.

    Models Used:
    - Product: Retrieves the product by ID.

    Handles:
    - Adding items with or without size selection.
    - Updating the item quantity if it already exists in the bag.

    Redirects:
    - The user back to the specified `redirect_url`.
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get("quantity"))
    redirect_url = request.POST.get("redirect_url")
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get("bag", {})

    if size:
        if item_id in bag:
            if size in bag[item_id]["items_by_size"]:
                bag[item_id]["items_by_size"][size] += quantity
                messages.success(
                    request,
                    f'Updated size {size.upper()} {product.name} quantity to '
                    f'{bag[item_id]["items_by_size"][size]}'
                )
            else:
                bag[item_id]["items_by_size"][size] = quantity
                messages.success(request, f'Added size {size.upper()}'
                                 '{product.name} to your bag')
        else:
            bag[item_id] = {"items_by_size": {size: quantity}}
            messages.success(request, f'Added size {size.upper()}'
                             '{product.name} to your bag')
    else:
        if item_id in bag:
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name}'
                             'quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session["bag"] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of a specified product in the shopping bag.

    Request Type:
    - POST: Modifies the product quantity in the session cart.

    Models Used:
    - Product: Retrieves the product by ID.

    Handles:
    - Adjusting the item quantity based on user input.
    - Removing an item if the quantity is reduced to zero.

    Redirects:
    - The user back to the shopping bag page.
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get("quantity"))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get("bag", {})

    if size:
        if quantity > 0:
            bag[item_id]["items_by_size"][size] = quantity
            messages.success(
                request,
                f'Updated size {size.upper()} {product.name} quantity to '
                f'{bag[item_id]["items_by_size"][size]}'
            )
        else:
            del bag[item_id]["items_by_size"][size]
            if not bag[item_id]["items_by_size"]:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()}'
                             '{product.name} from your bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name}'
                             'quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session["bag"] = bag
    return redirect(reverse("view_bag"))


def remove_from_bag(request, item_id):
    """
    Remove a product from the shopping bag.

    Request Type:
    - POST: Removes the product from the session cart.

    Models Used:
    - Product: Retrieves the product by ID.

    Handles:
    - Removing a product with or without size selection.
    - Providing error messages if an issue occurs.

    Response:
    - HTTP 200: If the product is successfully removed.
    - HTTP 500: If an error occurs during removal.
    """
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get("bag", {})

        if size:
            del bag[item_id]["items_by_size"][size]
            if not bag[item_id]["items_by_size"]:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()}'
                             '{product.name} from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session["bag"] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f"Error removing item: {e}")
        return HttpResponse(status=500)
