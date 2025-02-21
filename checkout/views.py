import json
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
    print("DEBUG: cache_checkout_data view reached")

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
        print(f"DEBUG: Cached checkout data for PID: {pid}")
        return HttpResponse(status=200)

    except Exception as e:
        print(f"DEBUG: Error in cache_checkout_data: {e}")
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
    print("DEBUG: checkout view reached")
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        print("DEBUG: Received POST request in checkout view")
        bag = request.session.get("bag", {})

        if not bag:
            messages.error(request, "There's nothing in"
                           "your bag at the moment")
            return redirect(reverse("products"))

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

        order_form = OrderForm(form_data)

        if order_form.is_valid():
            print("DEBUG: Order form is valid")
            order = order_form.save(commit=False)

            # Link the order to the user's profile if authenticated
            if request.user.is_authenticated:
                try:
                    profile = UserProfile.objects.get(user=request.user)
                    order.user_profile = profile
                except UserProfile.DoesNotExist:
                    messages.error(
                        request, "Profile not found."
                        "Please update your profile."
                    )
                    return redirect(reverse("profile"))

            pid = request.POST.get("client_secret").split("_secret")[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()

            print(f"DEBUG: Order created with order number: {order.order_number}")

            # Process each item in the bag
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    print(f"DEBUG: Found product - {product.name}")

                    if isinstance(item_data, int):
                        OrderLineItem.objects.create(
                            order=order, product=product, quantity=item_data
                        )
                    else:
                        for size, quantity in item_data["items_by_size"].items():
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
                    return redirect(reverse("view_bag"))

            request.session["save_info"] = "save-info" in request.POST
            return redirect(reverse
                            ("checkout_success", args=[order.order_number]))
            return redirect(reverse("checkout_success", args=[order.order_number]))
            messages.error(
                request, "There was an error with your form. "
                "Please double-check your information."
            )

    else:
        bag = request.session.get("bag", {})
        if not bag:
            messages.error(request, "There's nothing in"
                           "your bag at the moment")
            return redirect(reverse("products"))

        current_bag = bag_contents(request)
        total = current_bag["grand_total"]
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total, currency=settings.STRIPE_CURRENCY
        )

        order_form = OrderForm()
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    "full_name": profile.user.get_full_name(),
                    "email": profile.user.email,
                    "phone_number": profile.default_phone_number,
                    "country": profile.default_country,
                    "postcode": profile.default_postcode,
                    "town_or_city": profile.default_town_or_city,
                    "street_address1": profile.default_street_address1,
                    "street_address2": profile.default_street_address2,
                    "county": profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(
            request,
            "Stripe public key is missing."
            "Did you forget to set it in your environment?"
        )

    return render(
        request, "checkout/checkout.html",
        {
            "order_form": order_form,
            "stripe_public_key": stripe_public_key,
            "client_secret": intent.client_secret,
        }
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
    print(f"DEBUG: checkout_success view reached for order {order_number}")
    save_info = request.session.get("save_info")

    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)

        if order.user_profile == profile:
            if save_info:
                profile_data = {
                    "default_phone_number": order.phone_number,
                    "default_country": order.country,
                    "default_postcode": order.postcode,
                    "default_town_or_city": order.town_or_city,
                    "default_street_address1": order.street_address1,
                    "default_street_address2": order.street_address2,
                    "default_county": order.county,
                }
                user_profile_form = UserProfileForm(profile_data,
                                                    instance=profile)
                if user_profile_form.is_valid():
                    user_profile_form.save()

    messages.success(
        request,
        f"Order successfully processed! Your order number is {order_number}. "
        f"A confirmation email will be sent to {order.email}."
    )

    if "bag" in request.session:
        del request.session["bag"]

    return render(request, "checkout/checkout_success.html", {"order": order})