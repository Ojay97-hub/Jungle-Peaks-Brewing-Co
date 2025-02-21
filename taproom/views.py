# Standard Library Imports

# Django Imports
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
        - POST: Creates a new booking for the logged-in user.

    **Context Provided:**
        - `form`: A booking form for user input.

    **Workflow:**
        - Saves the booking and associates it with the logged-in user.
        - Redirects to `booking_success` upon successful submission.
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Link booking to user
            booking.save()

            messages.success(request, 'Booking has been successfully created.')
            return redirect('booking_success')  # Redirect to success page
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
