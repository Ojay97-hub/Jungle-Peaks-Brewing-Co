from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UserProfileForm
from .models import UserProfile
from checkout.models import Order, OrderLineItem
from products.models import Review
from taproom.models import Booking
from tours.models import TourBooking


@login_required
def profile(request):
    """
    Display and manage the user's profile.

    Models Used:
    - UserProfile: Retrieves user profile information.
    - Review: Fetches the reviews made by the logged-in user.
    - Order: Retrieves past orders for the logged-in user.
    - Booking: Fetches table bookings made by the user.
    - TourBooking: Fetches tour bookings made by the user.

    Template Used:
    - profiles/profile.html

    Handles:
    - Displaying user profile data.
    - Updating user profile information via a form.
    - Showing order history, table bookings, and tour bookings.
    """

    profile = get_object_or_404(UserProfile, user=request.user)
    user_reviews = Review.objects.filter(user=request.user)
    orders = profile.orders.all()
    table_bookings = Booking.objects.filter(user=request.user)
    tour_bookings = TourBooking.objects.filter(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure'
                           'the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'orders': orders,
        'table_bookings': table_bookings,
        'tour_bookings': tour_bookings,
        'reviews': user_reviews,
        'on_profile_page': True,
    }

    return render(request, 'profiles/profile.html', context)


def order_history(request, order_number):
    """
    Display past order details.

    Models Used:
    - Order: Retrieves the specific order by order number.

    Template Used:
    - checkout/checkout_success.html

    Handles:
    - Fetching an order based on order_number.
    - Displaying order details.
    - Notifying the user that this is a past order confirmation.
    """

    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, 'checkout/checkout_success.html', context)


@login_required
def reorder(request, order_id):
    """
    Add items from a previous order to the current session shopping bag and redirect to the bag view.
    
    Fetches the order belonging to the requesting user, merges its line items into the session 'bag' (summing quantities for matching products), saves the updated bag in the session, and redirects the user to the shopping bag page.
    
    Parameters:
        order_id (int): Database ID of the order to re-add to the bag.
    
    Returns:
        HttpResponseRedirect: Redirect response to the shopping bag view.
    """

    order = get_object_or_404(Order,
                              id=order_id,
                              user_profile=request.user.userprofile)

    # Retrieve the user's shopping bag from session
    bag = request.session.get('bag', {})

    # Add past order items to the shopping bag
    for item in OrderLineItem.objects.filter(order=order):
        product_id = str(item.product.id)
        quantity = item.quantity

        if product_id in bag:
            bag[product_id] += quantity
        else:
            bag[product_id] = quantity

    # Save updated bag to session
    request.session['bag'] = bag

    messages.success(request, "Your previous order has been added to your bag. You can now proceed to checkout.")

    return redirect('bag:view_bag')