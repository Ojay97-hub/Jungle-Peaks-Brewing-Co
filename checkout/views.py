from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem

from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from bag.contexts import bag_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):
    print("DEBUG: cache_checkout_data view reached")
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': str(request.user),
        })
        print(f"DEBUG: Cached checkout data for PID: {pid}")
        return HttpResponse(status=200)
    except Exception as e:
        print(f"DEBUG: Error in cache_checkout_data: {e}")
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    print("DEBUG: checkout view reached")
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        print("DEBUG: Received POST request in checkout view")
        bag = request.session.get('bag', {})

        if not bag:
            print("DEBUG: Bag is empty, redirecting to products")
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            print("DEBUG: Order form is valid")
            order = order_form.save(commit=False)

            # Ensure the order is linked to the user's profile
            if request.user.is_authenticated:
                try:
                    # Get the user's profile and associate it with the order
                    profile = UserProfile.objects.get(user=request.user)
                    order.user_profile = profile  # Link the order to the user's profile
                except UserProfile.DoesNotExist:
                    print("DEBUG: UserProfile does not exist.")
                    messages.error(request, "Profile not found. Please update your profile details.")
                    return redirect(reverse('profile'))

            # Continue with the existing logic:
            pid = request.POST.get('client_secret').split('_secret')[0]
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
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                        print(f"DEBUG: Order line item added for product {product.name}, quantity {item_data}")
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                            print(f"DEBUG: Order line item added for product {product.name}, size {size}, quantity {quantity}")

                except Product.DoesNotExist:
                    print(f"DEBUG: Product with ID {item_id} does not exist")
                    messages.error(request, "One of the products in your bag wasn't found in our database. Please call us for assistance!")
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            print(f"DEBUG: Redirecting to checkout_success with order number {order.order_number}")
            return redirect(reverse('checkout_success', args=[order.order_number]))

        else:
            print(f"DEBUG: Order form is invalid, errors: {order_form.errors}")
            messages.error(request, 'There was an error with your form. Please double-check your information.')

    else:
        print("DEBUG: Received GET request in checkout view")
        bag = request.session.get('bag', {})
        if not bag:
            print("DEBUG: Bag is empty, redirecting to products")
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        print(f"DEBUG: Stripe PaymentIntent created with amount {stripe_total}")

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
                print(f"DEBUG: Prefilled order form for user {request.user}")
            except UserProfile.DoesNotExist:
                print("DEBUG: User profile does not exist, using empty form")
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        print("DEBUG: Stripe public key is missing!")
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    print(f"DEBUG: checkout_success view reached for order {order_number}")
    save_info = request.session.get('save_info')

    try:
        order = get_object_or_404(Order, order_number=order_number)
        print(f"DEBUG: Order {order_number} found")
    except Exception as e:
        print(f"DEBUG: Error fetching order: {e}")
        messages.error(request, "Error retrieving your order. Please contact support.")
        return redirect(reverse('home'))

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)

        if order.user_profile == profile:
            print(f"DEBUG: Order belongs to authenticated user {request.user}")

            if save_info:
                profile_data = {
                    'default_phone_number': order.phone_number,
                    'default_country': order.country,
                    'default_postcode': order.postcode,
                    'default_town_or_city': order.town_or_city,
                    'default_street_address1': order.street_address1,
                    'default_street_address2': order.street_address2,
                    'default_county': order.county,
                }
                user_profile_form = UserProfileForm(profile_data, instance=profile)
                if user_profile_form.is_valid():
                    user_profile_form.save()
                    print("DEBUG: User profile updated with order details")

    messages.success(request, f'Order successfully processed! Your order number is {order_number}. A confirmation email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']
        print("DEBUG: Bag cleared from session after successful checkout")

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
