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


SLUG_TO_KEY = {
    "guided-brewery-tour": "guided",
    "sunset-tour": "sunset",
    "craft-beer-tasting": "craft_tasting",
    "seasonal-selection": "seasonal",
    "master-brewer-session": "brewer_session",
}
KEY_TO_SLUG = {v: k for k, v in SLUG_TO_KEY.items()}

def tours(request):
    """
    View to display the available tours.
    """
    return render(request, "tours/tours.html")


@login_required
def book_tour(request, tour_slug=None):
    """
    Handles the tour booking process.
    """
    # If the route passes a pretty slug, convert it to the backend key for the form
    initial_data = {}
    if tour_slug:
        initial_data["tour"] = SLUG_TO_KEY.get(tour_slug, None)

    if request.method == "POST":
        form = TourBookingForm(request.POST, initial=initial_data)
        if form.is_valid():
            booking = form.save(commit=False)

            selected_tour = booking.tour                 # e.g. 'craft_tasting'
            booking_date = booking.date
            guests_requested = booking.guests

            # Human-friendly name
            tour_display_name = dict(TOUR_CHOICES).get(selected_tour, "Unknown Tour")

            # How many seats are already confirmed for that date/tour
            booked_guests = (
                TourBooking.objects
                .filter(tour=selected_tour, date=booking_date, status="confirmed")
                .aggregate(Sum("guests"))["guests__sum"] or 0
            )
            capacity = TOUR_CAPACITY.get(selected_tour, 0)
            available_slots = max(capacity - booked_guests, 0)

            if guests_requested > available_slots:
                messages.error(
                    request,
                    f"❌ Sorry, only {available_slots} spots left for {tour_display_name} on {booking_date}."
                )
                # If you use pretty slugs in your URL, redirect with slug again:
                return redirect("book_tour", tour_slug=KEY_TO_SLUG.get(selected_tour, selected_tour))

            # All good → confirm and save
            booking.user = request.user
            booking.status = "confirmed"
            booking.save()  # model-level guard still prevents race-condition overbooking

            messages.success(
                request,
                f"🎉 Your {tour_display_name} booking on {booking_date} is confirmed!"
            )
            return redirect("tour_booking_success", booking_id=booking.id)
    else:
        form = TourBookingForm(initial=initial_data)

    return render(request, "tours/book_tour.html", {"form": form})


def tour_booking_success(request, booking_id):
    """
    Displays a success message and booking details after a successful booking.
    """
    booking = get_object_or_404(TourBooking, id=booking_id)
    return render(
        request, "tours/tour_booking_success.html", {"booking": booking}
    )


def check_availability(request):
    """
    API endpoint to check real-time availability for a selected tour date.
    """
    tour = request.GET.get("tour")
    booking_date = request.GET.get("date")

    if not tour or not booking_date:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    booked_guests = TourBooking.objects.filter(
        tour=tour, date=booking_date, status="confirmed"
    ).aggregate(Sum("guests"))["guests__sum"] or 0

    available_slots = TOUR_CAPACITY.get(tour, 0) - booked_guests

    return JsonResponse({"available_slots": available_slots})


@login_required
def edit_booking(request, booking_id):
    """
    Allows a user to edit an existing tour booking.
    """
    booking = get_object_or_404(TourBooking, id=booking_id, user=request.user)

    if request.method == "POST":
        form = TourBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your tour booking has been updated successfully.",
            )
            return redirect("profile")  # Redirect to profile page
    else:
        form = TourBookingForm(instance=booking)

    return render(request, "tours/edit_booking.html", {"form": form})


@login_required
def cancel_booking(request, booking_id):
    """
    Cancels an existing tour booking.
    """
    booking = get_object_or_404(TourBooking, id=booking_id, user=request.user)

    # Only allow POST requests for security
    if request.method == "POST":
        booking.delete()
        messages.success(
            request,
            "Your tour booking has been successfully canceled.",
        )
    else:
        messages.error(request, "Invalid request method.")

    return redirect("profile")  # Redirect back to profile page
