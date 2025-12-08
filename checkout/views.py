import json
import logging

import stripe

from django.conf import settings
from django.contrib import messages
from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.views.decorators.http import require_POST

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from bag.contexts import bag_contents
from bag.models import Cart, CartItem
from django.contrib.auth.models import User
from tours.models import TourBooking
from taproom.models import Booking
from .utils import send_order_confirmation_email


logger = logging.getLogger(__name__)


def clear_user_cart(username):
    """Clear the user's shopping cart after successful order."""
    try:
        if username:
            user = User.objects.get(username=username)
            # Delete all cart items for this user
            cart_items = CartItem.objects.filter(cart__user=user)
            cart_items.delete()
            # Note: The Cart object itself is kept for future use
    except Exception as e:
        # Log the error but don't fail
        logger.warning(f"Could not clear cart for user {username}: {e}")


@require_POST
def cache_checkout_data(request):
    """
    Store checkout data in Stripe's PaymentIntent metadata.

    Request Type:
    - POST: Stores cart data in Stripe for validation.

    Models Used:
    - Order: Stores the checkout order details.

    API Used:
    - Stripe PaymentIntent API.

    Response:
    - HTTP 200: If data caching is successful.
    - HTTP 400: If an error occurs while caching data.
    """
    try:
        pid = request.POST.get("client_secret").split("_secret")[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "bag": json.dumps(request.session.get("bag", {})),
                "save_info": request.POST.get("save_info"),
                "username": str(request.user),
            },
        )
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(
            request,
            "Sorry, your payment cannot be processed right now. "
            "Please try again later."
        )
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    Handle the checkout process, including order creation.

    Request Type:
    - GET: Displays the checkout form.
    - POST: Processes the order and payment.

    Models Used:
    - Order: Stores the checkout order details.
    - OrderLineItem: Stores items linked to an order.
    - Product: Retrieves product details.
    - UserProfile: Retrieves user profile information.

    API Used:
    - Stripe PaymentIntent API.

    Template Used:
    - checkout/checkout.html

    Redirects:
    - checkout_success: If the order is successful.
    - view_bag: If a product in the cart is invalid.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        # Get database cart items first
        cart_items = []
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                cart_items = CartItem.objects.filter(cart=cart)
            except Cart.DoesNotExist:
                pass

        # Also check session bag for backward compatibility
        bag = request.session.get("bag", {})

        if not cart_items and not bag:
            messages.error(
                request,
                "There's nothing in your bag at the moment."
            )
            return redirect(reverse("products"))

        # Calculate bag contents to check for physical products
        current_bag = bag_contents(request)
        product_count = current_bag['product_count']

        if product_count > 0:
            form_data = {
                "full_name": request.POST["full_name"],
                "email": request.POST["email"],
                "phone_number": request.POST["phone_number"],
                "country": request.POST["country"],
                "postcode": request.POST["postcode"],
                "town_or_city": request.POST["town_or_city"],
                "street_address1": request.POST["street_address1"],
                "street_address2": request.POST["street_address2"],
                "county": request.POST["county"],
            }
        else:
            # Digital orders (Tours/Taproom) don't need entry address
            form_data = {
                "full_name": request.POST["full_name"],
                "email": request.POST["email"],
                "phone_number": request.POST["phone_number"],
                # Fill required fields with dummy data for validation
                "country": "GB", 
                "postcode": "N/A",
                "town_or_city": "Digital Delivery",
                "street_address1": "Digital Delivery",
                "street_address2": "",
                "county": "",
            }

        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save(commit=False)

            if request.user.is_authenticated:
                try:
                    profile = UserProfile.objects.get(user=request.user)
                    order.user_profile = profile
                except UserProfile.DoesNotExist:
                    messages.error(
                        request,
                        "Profile not found. Please update your profile."
                    )
                    return redirect(reverse("profile"))

            pid = request.POST.get("client_secret").split("_secret")[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()

            # Process database cart items first
            for cart_item in cart_items:
                if cart_item.item_type == 'product':
                    OrderLineItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        product_size=cart_item.size
                    )
                elif cart_item.item_type == 'tour' and cart_item.tour_booking:
                    # Update booking contact details from order
                    cart_item.tour_booking.name = order.full_name
                    cart_item.tour_booking.email = order.email
                    cart_item.tour_booking.phone = order.phone_number
                    cart_item.tour_booking.save()
                    
                    # Create order line item for tour
                    OrderLineItem.objects.create(
                        order=order,
                        product=None,  # Tours don't have products
                        quantity=cart_item.tour_guests,
                        tour_booking=cart_item.tour_booking
                    )
                elif cart_item.item_type == 'taproom' and cart_item.taproom_booking:
                    # Update booking contact details from order
                    cart_item.taproom_booking.name = order.full_name
                    cart_item.taproom_booking.email = order.email
                    cart_item.taproom_booking.phone = order.phone_number
                    cart_item.taproom_booking.save()

                    # Create order line item for taproom booking
                    OrderLineItem.objects.create(
                        order=order,
                        product=None,  # Taproom bookings don't have products
                        quantity=1,  # One booking per line item
                        taproom_booking=cart_item.taproom_booking
                    )

            # Process session bag items (backward compatibility)
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        OrderLineItem.objects.create(
                            order=order, product=product, quantity=item_data
                        )
                    else:
                        for size, quantity in (
                            item_data.get("items_by_size", {}).items()
                        ):
                            OrderLineItem.objects.create(
                                order=order, product=product,
                                quantity=quantity, product_size=size
                            )
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "One of the products in your bag wasn't found. "
                        "Please call us for assistance!"
                    )
                    order.delete()
                    return redirect("/bag/")

            request.session["save_info"] = "save-info" in request.POST
            return redirect(
                reverse("checkout_success", args=[order.order_number])
            )
        else:
            messages.error(
                request,
                "There was an error with your form. "
                "Please double-check your information."
            )

    else:
        # Get database cart items for GET request
        cart_items = []
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                cart_items = CartItem.objects.filter(cart=cart)
            except Cart.DoesNotExist:
                pass

        # Also check session bag for backward compatibility
        bag = request.session.get("bag", {})

        if not cart_items and not bag:
            messages.error(
                request, "There's nothing in your bag at the moment."
            )
            return redirect(reverse("products"))

        current_bag = bag_contents(request)
        total = current_bag["grand_total"]
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total, currency=settings.STRIPE_CURRENCY
        )

        # Initialize order form
        order_form = OrderForm()
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                initial_data = {
                    "full_name": profile.user.get_full_name(),
                    "email": profile.user.email,
                    "phone_number": profile.default_phone_number,
                    "country": profile.default_country,
                    "postcode": profile.default_postcode,
                    "town_or_city": profile.default_town_or_city,
                    "street_address1": profile.default_street_address1,
                    "street_address2": profile.default_street_address2,
                    "county": profile.default_county,
                }
                
                # Check if we need to supplement missing contact info from bookings in cart
                if not initial_data["phone_number"] or not initial_data["full_name"]:
                    try:
                        # Inspect cart items for booking details
                        # Get cart items directly from database
                        try:
                            cart = Cart.objects.get(user=request.user)
                            cart_items = CartItem.objects.filter(cart=cart)
                        except Cart.DoesNotExist:
                            cart_items = []
                        
                        for item in cart_items:
                            booking = None
                            if item.item_type == 'tour' and item.tour_booking:
                                booking = item.tour_booking
                            elif item.item_type == 'taproom' and item.taproom_booking:
                                booking = item.taproom_booking
                            
                            if booking:
                                # Found a booking, use its contact info if ours is missing
                                if not initial_data["full_name"] and booking.name:
                                    initial_data["full_name"] = booking.name
                                if not initial_data["phone_number"] and booking.phone:
                                    initial_data["phone_number"] = booking.phone
                                # If we found what we needed, break
                                if initial_data["full_name"] and initial_data["phone_number"]:
                                    break
                    except Exception as e:
                        # If anything fails in looking up bookings, just proceed with profile data
                        pass

                order_form = OrderForm(initial=initial_data)
            except UserProfile.DoesNotExist:
                order_form = OrderForm()

        # Add bag contents to template context
        template_context = {
            "order_form": order_form,
            "stripe_public_key": stripe_public_key,
            "client_secret": intent.client_secret,
            "bag_items": current_bag["bag_items"],
            "total": current_bag["total"],
            "delivery": current_bag["delivery"],
            "grand_total": current_bag["grand_total"],
        }

    if not stripe_public_key:
        messages.warning(
            request,
            "Stripe public key is missing. "
            "Did you forget to set it in your environment?"
        )

    return render(
        request, "checkout/checkout.html",
        template_context
    )


def checkout_success(request, order_number):
    """
    Handle successful checkouts.

    Models Used:
    - Order: Retrieves the successfully placed order.
    - UserProfile: Updates profile details if save_info is set.

    Template Used:
    - checkout/checkout_success.html

    Redirects:
    - home: If the order is not found.
    """
    order = get_object_or_404(Order, order_number=order_number)
    save_info = request.session.get("save_info")

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        if order.user_profile == profile and save_info:
            profile_data = {
                "default_phone_number": order.phone_number,
                "default_country": order.country,
                "default_postcode": order.postcode,
                "default_town_or_city": order.town_or_city,
                "default_street_address1": order.street_address1,
                "default_street_address2": order.street_address2,
                "default_county": order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

        # Clear the user's cart after successful order
        clear_user_cart(request.user.username)

    sent_orders = request.session.get("orders_with_sent_email", [])
    should_send_email = order_number not in sent_orders

    email_sent = False
    if should_send_email:
        try:
            email_sent = bool(send_order_confirmation_email(order))
        except Exception:
            logger.exception(
                "Failed to send confirmation email for order %s", order_number
            )
            messages.warning(
                request,
                (
                    "Your order was processed, but we couldn't send a confirmation "
                    "email. Please contact us if you don't receive one shortly."
                ),
            )
        else:
            if email_sent:
                sent_orders.append(order_number)
                request.session["orders_with_sent_email"] = sent_orders[-10:]

    success_message = f"Order successfully processed! Your order number is {order_number}."
    if email_sent:
        success_message += f" A confirmation email was sent to {order.email}."

    messages.success(request, success_message)

    recent_orders = request.session.get("recent_orders", [])
    if order_number not in recent_orders:
        recent_orders.append(order_number)
        request.session["recent_orders"] = recent_orders[-5:]

    if "bag" in request.session:
        del request.session["bag"]

    return render(request, "checkout/checkout_success.html", {"order": order})


@require_POST
def resend_order_confirmation(request, order_number):
    """Allow customers to trigger an additional confirmation email."""
    order = get_object_or_404(Order, order_number=order_number)

    allowed = False
    if request.user.is_authenticated and order.user_profile:
        allowed = order.user_profile.user == request.user

    recent_orders = request.session.get("recent_orders", [])
    if order_number in recent_orders:
        allowed = True

    if not allowed:
        messages.error(
            request,
            "We couldn't verify permission to resend that order confirmation.",
        )
        return redirect("home")

    try:
        send_order_confirmation_email(order)
        sent_orders = request.session.get("orders_with_sent_email", [])
        if order_number not in sent_orders:
            sent_orders.append(order_number)
            request.session["orders_with_sent_email"] = sent_orders[-10:]
        messages.success(
            request,
            f"A confirmation email was resent to {order.email}.",
        )
    except Exception:
        logger.exception("Failed to resend confirmation email for order %s", order_number)
        messages.warning(
            request,
            "We couldn't resend the confirmation email right now. Please try again later.",
        )

    return redirect("checkout_success", order_number=order_number)
