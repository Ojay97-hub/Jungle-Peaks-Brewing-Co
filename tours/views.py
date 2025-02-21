# Standard Library Imports
from datetime import date

# Django Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum

# Local Application Imports
from .forms import TourBookingForm
from .models import TourBooking, TOUR_CAPACITY, TOUR_CHOICES


def tours(request):
    """
    View to display the available tours.

    **Template Used:**
        - `tours/tours.html`

    **Request Method Supported:**
        - GET: Displays the list of tours.

    **Context Provided:**
        - None (Modify to include tours data if needed).
    """
    return render(request, 'tours/tours.html')


def book_tour(request, tour_slug=None):
    """
    Handles the tour booking process.

    **Models Used:**
        - `TourBooking`

    **Templates Used:**
        - `tours/book_tour.html`

    **Request Methods Supported:**
        - GET: Displays the booking form
        (pre-filled if `tour_slug` is provided).
        - POST: Processes booking submission.

    **Context Provided:**
        - `form`: Tour booking form.

    **Booking Workflow:**
        - Checks tour availability before confirming.
        - Automatically confirms the booking if slots are available.
        - Redirects to `tour_booking_success` if successful.
    """
    initial_data = {"tour": tour_slug} if tour_slug else {}

    if request.method == "POST":
        form = TourBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Link to the logged-in user
            booking.save()

            # ✅ Check availability dynamically
            selected_tour = booking.tour
            booking_date = booking.date
            guests_requested = booking.guests

            # 🛠 Fix: Use `dict(TOUR_CHOICES)` to get the tour name properly
            tour_display_name = dict(TOUR_CHOICES).get
            (selected_tour, "Unknown Tour")

            booked_guests = TourBooking.objects.filter(
                tour=selected_tour, date=booking_date, status="confirmed"
            ).aggregate(Sum('guests'))['guests__sum'] or 0

            available_slots = TOUR_CAPACITY.get
            (selected_tour, 0) - booked_guests

            if guests_requested > available_slots:
                messages.error(
                    request,
                    f"❌ Sorry, only {available_slots} spots left "
                    f"for {tour_display_name} on {booking_date}."
                )
                return redirect("book_tour", tour_slug=selected_tour)

            # ✅ Automatically confirm booking
            booking.status = "confirmed"
            booking.save()
            messages.success(
                request,
                f"🎉 Your {tour_display_name} booking"
                "on {booking_date} is confirmed!"
            )

            # 🔄 Redirect to success page with booking details
            return redirect("tour_booking_success", booking_id=booking.id)

    else:
        form = TourBookingForm(initial=initial_data)

    return render(request, "tours/book_tour.html", {"form": form})


def tour_booking_success(request, booking_id):
    """
    Displays a success message and booking details after a successful booking.

    **Models Used:**
        - `TourBooking`

    **Templates Used:**
        - `tours/tour_booking_success.html`

    **Request Method Supported:**
        - GET: Retrieves the specific booking details.

    **Context Provided:**
        - `booking`: The confirmed booking details.
    """
    booking = get_object_or_404(TourBooking, id=booking_id)

    return render(request,
                  "tours/tour_booking_success.html", {"booking": booking})


def check_availability(request):
    """
    API endpoint to check real-time availability for a selected tour date.

    **Models Used:**
        - `TourBooking`

    **Request Method Supported:**
        - GET: Requires `tour` and `date` parameters.

    **Returns:**
        - JSON response with `available_slots`.

    **Example Response:**
    ```json
    {
        "available_slots": 5
    }
    ```
    """
    tour = request.GET.get("tour")
    booking_date = request.GET.get("date")

    if not tour or not booking_date:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    booked_guests = TourBooking.objects.filter(
        tour=tour, date=booking_date, status="confirmed"
    ).aggregate(Sum('guests'))['guests__sum'] or 0

    available_slots = TOUR_CAPACITY.get(tour, 0) - booked_guests

    return JsonResponse({"available_slots": available_slots})


@login_required
def edit_booking(request, booking_id):
    """
    Allows a user to edit an existing tour booking.

    **Models Used:**
        - `TourBooking`

    **Templates Used:**
        - `tours/edit_booking.html`

    **Request Methods Supported:**
        - GET: Displays the booking form pre-filled with existing details.
        - POST: Updates the booking details.

    **Context Provided:**
        - `form`: Pre-filled booking form.

    **Redirects:**
        - On success, redirects to `profile`.
    """
    booking = get_object_or_404(TourBooking, id=booking_id, user=request.user)

    if request.method == "POST":
        form = TourBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "Your tour booking has been"
                             "updated successfully.")
            return redirect("profile")  # Redirect to profile page
    else:
        form = TourBookingForm(instance=booking)

    return render(request, "tours/edit_booking.html", {"form": form})


@login_required
def cancel_booking(request, booking_id):
    """
    Cancels an existing tour booking.

    **Models Used:**
        - `TourBooking`

    **Request Methods Supported:**
        - POST: Cancels the booking.
        - GET: Shows an error message (invalid request).

    **Redirects:**
        - On success, redirects to `profile`.

    **Security Measures:**
        - Only allows POST requests to prevent accidental cancellations.
        - Ensures the logged-in user is the owner of the booking.

    **Success Message:**
        - "Your tour booking has been successfully canceled."
    """
    booking = get_object_or_404(TourBooking, id=booking_id, user=request.user)

    # Only allow POST requests for security
    if request.method == "POST":
        booking.delete()
        messages.success(request,
                         "Your tour booking has been successfully canceled.")
    else:
        messages.error(request, "Invalid request method.")

    return redirect("profile")  # Redirect back to profile page