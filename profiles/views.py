from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order, OrderLineItem
from products.models import Review
from taproom.models import Booking
from tours.models import TourBooking


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
    user_reviews = Review.objects.filter(user=request.user)  # Fetch reviews for logged-in user
    orders = profile.orders.all()  # Fetch user's order history
    
     # New queries for bookings:
    table_bookings = Booking.objects.filter(user=request.user)
    tour_bookings = TourBooking.objects.filter(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    # Pass all required data to the template
    context = {
        'form': form,
        'orders': orders,
        'table_bookings': table_bookings,
        'tour_bookings': tour_bookings,
        'reviews': user_reviews,  # Use 'reviews' instead of 'user_reviews' to match template variable
        'on_profile_page': True,
    }

    return render(request, 'profiles/profile.html', context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)

@login_required
def reorder(request, order_id):
    """
    Allows users to reorder a past purchase by adding the same items back to the bag.
    """
    order = get_object_or_404(Order, id=order_id, user_profile=request.user.userprofile)

    # Retrieve the user's bag from the session or create an empty one
    bag = request.session.get('bag', {})

    for item in OrderLineItem.objects.filter(order=order):
        product_id = str(item.product.id)
        quantity = item.quantity

        # Add to bag (if item already exists, update quantity)
        if product_id in bag:
            bag[product_id] += quantity
        else:
            bag[product_id] = quantity

    # Save updated bag to session
    request.session['bag'] = bag
    messages.success(request, "Your previous order has been added to your bag. You can now proceed to checkout.")
    
    return redirect('view_bag')  # Redirect to shopping bag page

