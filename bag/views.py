from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime

from products.models import Product
from tours.models import TourBooking, TOUR_CAPACITY
from taproom.models import Booking
from profiles.models import UserProfile
from .models import Cart, CartItem


def view_bag(request):
    """
    Display the shopping bag page.
    """
    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """
    Add a specified quantity of a product to the shopping bag.
    """
    # Extract actual product ID from prefixed item_id (e.g., "product_4" -> 4)
    actual_item_id = item_id.replace('product_', '') if item_id.startswith('product_') else item_id
    product = get_object_or_404(Product, pk=actual_item_id)
    quantity = int(request.POST.get("quantity"))
    redirect_url = request.POST.get("redirect_url")
    size = None
    if "product_size" in request.POST:
        size = request.POST["product_size"]

    try:
        # Get or create user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if product already exists in cart
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            item_type='product',
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )

        if not item_created:
            # Product already exists, update quantity
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(
            request,
            f"Added {product.name} to your bag",
        )

    except Exception as e:
        # Fallback to session-based cart for backward compatibility
        bag = request.session.get("bag", {})

        if size:
            if item_id in bag:
                if size in bag[item_id]["items_by_size"]:
                    bag[item_id]["items_by_size"][size] += quantity
                else:
                    bag[item_id]["items_by_size"][size] = quantity
            else:
                bag[item_id] = {"items_by_size": {size: quantity}}
        else:
            if item_id in bag:
                bag[item_id] += quantity
            else:
                bag[item_id] = quantity

        request.session["bag"] = bag
        messages.success(
            request,
            f"Added {product.name} to your bag",
        )

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of a specified product in the shopping bag.
    """
    # Extract actual product ID from prefixed item_id (e.g., "product_4" -> 4)
    actual_item_id = item_id.replace('product_', '') if item_id.startswith('product_') else item_id
    product = get_object_or_404(Product, pk=actual_item_id)
    quantity = int(request.POST.get("quantity"))
    size = None
    if "product_size" in request.POST:
        size = request.POST["product_size"]

    try:
        # Get user's cart
        cart = Cart.objects.get(user=request.user)

        # Find the cart item
        cart_item = CartItem.objects.get(
            cart=cart,
            item_type='product',
            product=product,
            size=size
        )

        # Update quantity or delete if zero
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(
                request,
                f"Updated {product.name} quantity to {quantity}",
            )
        else:
            cart_item.delete()
            messages.success(
                request,
                f"Removed {product.name} from your bag",
            )

    except Cart.DoesNotExist:
        messages.error(request, "No cart found")
    except CartItem.DoesNotExist:
        messages.error(request, "Product not found in cart")
    except Exception as e:
        # Fallback to session-based cart
        bag = request.session.get("bag", {})

        if size:
            if item_id in bag and size in bag[item_id]["items_by_size"]:
                if quantity > 0:
                    bag[item_id]["items_by_size"][size] = quantity
                    messages.success(
                        request,
                        f"Updated size {size.upper()} {product.name} quantity to {quantity}",
                    )
                else:
                    del bag[item_id]["items_by_size"][size]
                    if not bag[item_id]["items_by_size"]:
                        bag.pop(item_id)
                    messages.success(
                        request,
                        f"Removed size {size.upper()} {product.name} from your bag",
                    )
        else:
            if item_id in bag:
                if quantity > 0:
                    bag[item_id] = quantity
                    messages.success(
                        request,
                        f"Updated {product.name} quantity to {quantity}",
                    )
                else:
                    bag.pop(item_id)
                    messages.success(
                        request,
                        f"Removed {product.name} from your bag",
                    )

        request.session["bag"] = bag

    return redirect(reverse("bag:view_bag"))


def remove_from_bag(request, item_id):
    """
    Remove a product from the shopping bag.
    """
    try:
        # Extract actual product ID from prefixed item_id (e.g., "product_4" -> 4)
        actual_item_id = item_id.replace('product_', '') if item_id.startswith('product_') else item_id
        product = get_object_or_404(Product, pk=actual_item_id)
        size = None
        if "product_size" in request.POST:
            size = request.POST["product_size"]

        # Try database cart first
        try:
            if not request.user.is_authenticated:
                raise Cart.DoesNotExist

            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(
                cart=cart,
                item_type='product',
                product=product,
                size=size
            )
            cart_item.delete()
            messages.success(
                request,
                f"Removed {product.name} from your bag",
            )
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            # Fallback to session cart
            bag = request.session.get("bag", {})

            if size:
                if item_id in bag and size in bag[item_id]["items_by_size"]:
                    del bag[item_id]["items_by_size"][size]
                    if not bag[item_id]["items_by_size"]:
                        bag.pop(item_id)
                    messages.success(
                        request,
                        f"Removed size {size.upper()} {product.name} from your bag",
                    )
            else:
                if item_id in bag:
                    bag.pop(item_id)
                    messages.success(
                        request,
                        f"Removed {product.name} from your bag",
                    )

            request.session["bag"] = bag

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return HttpResponse(status=200)
        return redirect(reverse("bag:view_bag"))

    except Exception as e:
        messages.error(
            request,
            f"Error removing item: {e}",
        )
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return HttpResponse(status=500)
        return redirect(reverse("bag:view_bag"))


@login_required
def add_tour_to_cart(request, tour_type, tour_date, guests):
    """
    Add a tour booking to the user's cart.
    """
    try:
        # Get or create user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Get user's phone number from profile
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_phone = user_profile.default_phone_number or ''
        except UserProfile.DoesNotExist:
            profile_phone = ''

        # Get contact info passed from booking form (if valid)
        booking_contact = request.session.pop('tour_booking_contact', {})
        
        booking_name = booking_contact.get('name') or request.user.get_full_name() or request.user.username
        booking_email = booking_contact.get('email') or request.user.email
        booking_phone = booking_contact.get('phone') or profile_phone

        # Create a temporary tour booking to validate availability
        tour_booking = TourBooking.objects.create(
            user=request.user,
            name=booking_name,
            email=booking_email,
            phone=booking_phone,
            tour=tour_type,
            date=tour_date,
            guests=guests,
            status='pending'
        )

        # Check availability
        booked_guests = (
            TourBooking.objects
            .filter(tour=tour_type, date=tour_date, status="confirmed")
            .aggregate(Sum("guests"))["guests__sum"] or 0
        )
        capacity = TOUR_CAPACITY.get(tour_type, 0)
        available_slots = max(capacity - booked_guests, 0)

        if guests > available_slots:
            tour_booking.delete()
            messages.error(
                request,
                f"Sorry, only {available_slots} spots left for this tour on {tour_date}."
            )
            return redirect(reverse("bag:view_bag"))

        # Create cart item for the tour
        cart_item = CartItem.objects.create(
            cart=cart,
            item_type='tour',
            tour_booking=tour_booking,
            tour_date=tour_date,
            tour_guests=guests
        )

        messages.success(
            request,
            f"Added {tour_booking.get_tour_display()} tour for {guests} guest(s) on {tour_date} to your cart"
        )

        return redirect(reverse("bag:view_bag"))

    except Exception as e:
        messages.error(
            request,
            f"Error adding tour to cart: {e}",
        )
        return redirect(reverse("bag:view_bag"))


@login_required
def add_taproom_to_cart(request, booking_type, booking_date, booking_time):
    """
    Add a taproom table booking to the user's cart.
    """
    try:
        # Parse date and time strings
        parsed_date = datetime.strptime(booking_date, '%Y-%m-%d').date()
        parsed_time = datetime.strptime(booking_time, '%H:%M').time()

        # Get or create user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Get user's phone number from profile
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_phone = user_profile.default_phone_number or ''
        except UserProfile.DoesNotExist:
            profile_phone = ''

        # Get contact info passed from booking form (if valid)
        booking_contact = request.session.pop('taproom_booking_contact', {})
        
        booking_name = booking_contact.get('name') or request.user.get_full_name() or request.user.username
        booking_email = booking_contact.get('email') or request.user.email
        booking_phone = booking_contact.get('phone') or profile_phone

        # Create a temporary taproom booking to validate availability
        taproom_booking = Booking.objects.create(
            user=request.user,
            name=booking_name,
            email=booking_email,
            phone=booking_phone,
            date=parsed_date,
            time=parsed_time,
            guests=booking_contact.get('guests', 1),  # Get guests from session
            booking_type=booking_type
        )

        # Create cart item for the taproom booking
        cart_item = CartItem.objects.create(
            cart=cart,
            item_type='taproom',
            taproom_booking=taproom_booking
        )

        booking_type_display = "Premium" if booking_type == "premium" else "Standard"
        messages.success(
            request,
            f"Added {booking_type_display} taproom booking for {parsed_date} at {parsed_time} to your cart"
        )

        return redirect(reverse("bag:view_bag"))

    except Exception as e:
        messages.error(
            request,
            f"Error adding taproom booking to cart: {e}",
        )
        return redirect(reverse("bag:view_bag"))


@login_required
def remove_tour_from_cart(request, cart_item_id):
    """
    Remove a tour from the shopping cart.
    """
    try:
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

        if cart_item.item_type == 'tour':
            # Get tour booking details before deletion for the success message
            tour_booking = None
            tour_display = "tour booking"

            try:
                tour_booking = cart_item.tour_booking
                if tour_booking and hasattr(tour_booking, 'get_tour_display'):
                    tour_display = f"{tour_booking.get_tour_display()} tour"
            except:
                pass

            # Try to delete the cart item and tour booking
            try:
                # Delete the cart item first
                cart_item_id = cart_item.id
                cart_item.delete()

                # Delete the associated tour booking if it exists
                if tour_booking:
                    try:
                        tour_booking.delete()
                    except Exception as tour_error:
                        # Log the error but don't fail the removal
                        print(f"Warning: Could not delete tour booking {tour_booking.id}: {tour_error}")

                messages.success(
                    request,
                    f"Removed {tour_display} from your cart"
                )

            except Exception as deletion_error:
                # If direct deletion fails, try a different approach
                try:
                    # Clear any foreign key relationships first
                    cart_item.tour_booking = None
                    cart_item.product = None
                    cart_item.save()

                    # Now try to delete
                    cart_item.delete()

                    if tour_booking:
                        try:
                            tour_booking.delete()
                        except:
                            pass

                    messages.success(
                        request,
                        f"Removed {tour_display} from your cart"
                    )

                except Exception as fallback_error:
                    # Last resort - just mark as deleted without actually removing
                    messages.warning(
                        request,
                        "Tour removed from cart view (may still exist in database)"
                    )
        else:
            messages.error(request, "Invalid cart item")

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return HttpResponse(status=200)
        return redirect(reverse("bag:view_bag"))

    except Exception as e:
        messages.error(
            request,
            f"Error removing tour from cart: {e}",
        )
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return HttpResponse(status=500)
        return redirect(reverse("bag:view_bag"))


@login_required
def remove_taproom_from_cart(request, cart_item_id):
    """
    Remove a taproom booking from the shopping cart.
    """
    try:
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

        if cart_item.item_type == 'taproom':
            # Get taproom booking details before deletion for the success message
            taproom_booking = None
            booking_display = "taproom booking"

            try:
                taproom_booking = cart_item.taproom_booking
                if taproom_booking:
                    booking_type_display = "Premium" if taproom_booking.booking_type == "premium" else "Standard"
                    booking_display = f"{booking_type_display} taproom booking"
            except:
                pass

            # Try to delete the cart item and taproom booking
            try:
                # Delete the cart item first
                cart_item_id = cart_item.id
                cart_item.delete()

                # Delete the associated taproom booking if it exists
                if taproom_booking:
                    try:
                        taproom_booking.delete()
                    except Exception as taproom_error:
                        # Log the error but don't fail the removal
                        print(f"Warning: Could not delete taproom booking {taproom_booking.id}: {taproom_error}")

                messages.success(
                    request,
                    f"Removed {booking_display} from your cart"
                )

            except Exception as deletion_error:
                # If direct deletion fails, try a different approach
                try:
                    # Clear any foreign key relationships first
                    cart_item.taproom_booking = None
                    cart_item.product = None
                    cart_item.save()

                    # Now try to delete
                    cart_item.delete()

                    if taproom_booking:
                        try:
                            taproom_booking.delete()
                        except:
                            pass

                    messages.success(
                        request,
                        f"Removed {booking_display} from your cart"
                    )

                except Exception as fallback_error:
                    # Last resort - just mark as deleted without actually removing
                    messages.warning(
                        request,
                        "Taproom booking removed from cart view (may still exist in database)"
                    )
        else:
            messages.error(request, "Invalid cart item")

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return HttpResponse(status=200)
        return redirect(reverse("bag:view_bag"))

    except Exception as e:
        messages.error(
            request,
            f"Error removing taproom booking from cart: {e}",
        )
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return HttpResponse(status=500)
        return redirect(reverse("bag:view_bag"))


@login_required
def remove_legacy_tour(request, item_id):
    """
    Remove a legacy tour item from the session cart.
    """
    try:
        # Get the session bag
        bag = request.session.get("bag", {})

        # Remove the legacy tour item from the session
        if item_id in bag:
            del bag[item_id]
            request.session["bag"] = bag

            messages.success(
                request,
                "Tour booking removed from your cart"
            )
        else:
            messages.error(request, "Tour booking not found in cart")

    except Exception as e:
        messages.error(request, f"Error removing tour booking: {e}")

    return redirect(reverse("bag:view_bag"))


@login_required
def migrate_tours_to_cart(request):
    """
    Migrate any tour items from session to database cart.
    """
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        session_bag = request.session.get("bag", {})
        migrated_count = 0

        for item_id, item_data in session_bag.items():
            if item_id.startswith('tour_'):
                # This is a tour item in session - try to migrate it
                try:
                    # Parse the tour data (assuming format: tour_type|tour_date|guests)
                    if isinstance(item_data, str):
                        tour_info = item_data.split('|')
                        if len(tour_info) >= 3:
                            tour_type = tour_info[0]
                            tour_date = tour_info[1]
                            guests = int(tour_info[2])

                            # Create a tour booking
                            tour_booking = TourBooking.objects.create(
                                user=request.user,
                                tour=tour_type,
                                date=tour_date,
                                guests=guests,
                                status='pending'
                            )

                            # Create cart item
                            CartItem.objects.create(
                                cart=cart,
                                item_type='tour',
                                tour_booking=tour_booking,
                                tour_date=tour_date,
                                tour_guests=guests
                            )

                            migrated_count += 1

                            # Remove from session
                            del session_bag[item_id]

                except Exception as e:
                    print(f"Error migrating tour item {item_id}: {e}")
                    continue

        # Save the updated session
        if migrated_count > 0:
            request.session["bag"] = session_bag
            messages.success(
                request,
                f"Migrated {migrated_count} tour item(s) to your cart"
            )
        else:
            messages.info(request, "No tour items found to migrate")

    except Exception as e:
        messages.error(request, f"Error migrating tour items: {e}")

    return redirect(reverse("bag:view_bag"))
