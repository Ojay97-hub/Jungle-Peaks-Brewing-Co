# Standard Library Imports

# Django Imports
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Local Application Imports
from taproom.models import Booking
from .forms import BookingForm


def taproom(request):
    """
    Displays the taproom homepage.

    **Template Used:**
        - `taproom/taproom.html`

    **Request Method Supported:**
        - GET: Renders the taproom page.
    """
    return render(request, 'taproom/taproom.html')


@login_required
def booking(request):
    """
    Allows a logged-in user to book a table in the taproom.

    **Models Used:**
        - `Booking`

    **Templates Used:**
        - `taproom/taproom_booking.html`

    **Request Methods Supported:**
        - GET: Displays the booking form.
        - POST: Creates a new booking and adds it to the user's cart.

    **Context Provided:**
        - `form`: A booking form for user input.

    **Workflow:**
        - Creates a temporary booking and adds it to the user's shopping cart.
        - Redirects to cart upon successful submission.
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Get form data
            booking_type = form.cleaned_data['booking_type']
            booking_date = form.cleaned_data['date']
            booking_time = form.cleaned_data['time']

            # Store contact info in session to pass to bag view and checkout
            request.session['taproom_booking_contact'] = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone']
            }

            # Create URL for adding taproom booking to cart
            # Format date as YYYY-MM-DD and time as HH:MM for URL safety
            formatted_date = booking_date.strftime('%Y-%m-%d')
            formatted_time = booking_time.strftime('%H:%M')
            cart_url = reverse('bag:add_taproom_to_cart',
                             args=[booking_type, formatted_date, formatted_time])

            return redirect(cart_url)
    else:
        form = BookingForm()

    return render(request, 'taproom/taproom_booking.html', {'form': form})


def booking_success(request):
    """
    Displays a success message after a successful booking.

    **Templates Used:**
        - `taproom/booking_success.html`

    **Request Method Supported:**
        - GET: Shows a confirmation message.

    **Context Provided:**
        - None
    """
    return render(request, "taproom/booking_success.html")


@login_required
def edit_booking(request, booking_id):
    """
    Allows a user to edit an existing taproom booking.

    **Models Used:**
        - `Booking`

    **Templates Used:**
        - `taproom/edit_booking.html`

    **Request Methods Supported:**
        - GET: Displays the booking form pre-filled with existing details.
        - POST: Updates the booking details.

    **Context Provided:**
        - `form`: A pre-filled booking form.

    **Workflow:**
        - Ensures the logged-in user owns the booking.
        - Saves changes and redirects to the user's profile.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Your booking has been updated successfully.")
            return redirect("profile")  # Redirect to profile page
    else:
        form = BookingForm(instance=booking)

    return render(request, "taproom/edit_booking.html", {"form": form})


@login_required
def cancel_booking(request, booking_id):
    """
    Allows a user to cancel their booking without a confirmation page.

    **Models Used:**
        - `Booking`

    **Request Method Supported:**
        - POST: Cancels the booking.

    **Redirects:**
        - On success, redirects the user to `profile`.

    **Security Measures:**
        - Ensures the logged-in user owns the booking.

    **Workflow:**
        - Deletes the booking and displays a success message.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    booking.delete()
    messages.success(request, "Your booking has been cancelled successfully!")

    return redirect("profile")  # Redirect user back to their profile


def get_booked_tables(request):
    """
    API Validates availability for tables on specific date/time
    Returns list of booked table IDs
    """
    date_str = request.GET.get('date')
    time_str = request.GET.get('time')
    
    if not date_str or not time_str:
        return JsonResponse({'booked_tables': []})
        
    # Convert string to date object if needed, or rely on Django's filter handling (usually string works for date field)
    booked_tables = Booking.objects.filter(
        date=date_str,
        time=time_str
    ).exclude(table_number__isnull=True).values_list('table_number', flat=True)
    
    return JsonResponse({'booked_tables': list(booked_tables)})
