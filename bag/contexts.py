from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem


def bag_contents(request):
    """Generate shopping bag context for templates."""
    bag_items = []
    total = 0
    product_count = 0
    tour_count = 0

    # Check if user is authenticated and has a cart
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)

            for cart_item in cart_items:
                if cart_item.item_type == 'product':
                    total += cart_item.price
                    product_count += cart_item.quantity
                    bag_items.append({
                        "item_id": f"product_{cart_item.product.id}",
                        "quantity": cart_item.quantity,
                        "product": cart_item.product,
                        "size": cart_item.size,
                        "cart_item_id": cart_item.id,
                        "item_type": "product",
                        "price": cart_item.price,  # ✅ Add price for consistent template access
                    })
                elif cart_item.item_type == 'tour':
                    # Use TourBooking data for display, fallback to CartItem fields
                    tour_booking = cart_item.tour_booking
                    total += tour_booking.get_total_price() if tour_booking else 0
                    tour_count += cart_item.tour_guests or (tour_booking.guests if tour_booking else 0)

                    bag_items.append({
                        "item_id": f"tour_{cart_item.tour_booking.id}",
                        "tour_booking": tour_booking,
                        "tour_date": cart_item.tour_date or (tour_booking.date if tour_booking else None),
                        "tour_guests": cart_item.tour_guests or (tour_booking.guests if tour_booking else 0),
                        "cart_item_id": cart_item.id,
                        "item_type": "tour",
                        "price": tour_booking.get_total_price() if tour_booking else 0,
                    })
                elif cart_item.item_type == 'taproom':
                    # Use Booking data for display
                    taproom_booking = cart_item.taproom_booking
                    total += taproom_booking.get_total_price() if taproom_booking else 0

                    bag_items.append({
                        "item_id": f"taproom_{cart_item.taproom_booking.id}",
                        "taproom_booking": taproom_booking,
                        "cart_item_id": cart_item.id,
                        "item_type": "taproom",
                        "price": taproom_booking.get_total_price() if taproom_booking else 0,
                    })
        except Cart.DoesNotExist:
            # User doesn't have a cart yet, create one
            cart = Cart.objects.create(user=request.user)

        except Exception as e:
            # Log any other errors that might occur
            print(f"Error retrieving cart for user {request.user.username}: {e}")
            # Still fall back to session cart

    # Fallback to session-based cart for backward compatibility
    if not bag_items:
        bag = request.session.get("bag", {})

        for item_id, item_data in bag.items():
            # Check if this might be a tour item (starts with 'tour_')
            if item_id.startswith('tour_'):
                # Handle legacy tour items in session - mark as removable
                bag_items.append({
                    "item_id": item_id,
                    "item_type": "tour",
                    "cart_item_id": None,
                    "legacy_item": True,  # ✅ Ensure this is always set for session tour items
                    "price": 0,           # ✅ Avoid blank "£" in template
                })
                continue

            try:
                product = Product.objects.get(pk=item_id)
            except Product.DoesNotExist:
                continue  # Skip the missing product instead of raising 404
            if isinstance(item_data, int):
                total += item_data * product.price
                product_count += item_data
                bag_items.append(
                    {
                        "item_id": item_id,
                        "quantity": item_data,
                        "product": product,
                        "item_type": "product",
                        "price": item_data * product.price,
                    }
                )
            else:
                for size, quantity in item_data["items_by_size"].items():
                    total += quantity * product.price
                    product_count += quantity
                    bag_items.append(
                        {
                            "item_id": item_id,
                            "quantity": quantity,
                            "product": product,
                            "size": size,
                            "item_type": "product",
                            "price": quantity * product.price,
                        }
                    )

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(
            settings.STANDARD_DELIVERY_PERCENTAGE / 100
        )
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "tour_count": tour_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        "grand_total": grand_total,
    }

    return context
