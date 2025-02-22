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
    """
    return render(request, "tours/tours.html")


@login_required
def book_tour(request, tour_slug=None):
    """
    Handles the tour booking process.
    """
    initial_data = {"tour": tour_slug} if tour_slug else {}

    if request.method == "POST":
        form = TourBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            if not request.user.is_authenticated:
                messages.error(
                    request,
                    "You must be logged in to book a tour.",
                )
                return redirect("login")  # Redirect to login page

            booking.user = request.user  # Link to the logged-in user
            booking.save()

            # ✅ Check availability dynamically
            selected_tour = booking.tour
            booking_date = booking.date
            guests_requested = booking.guests

            # 🛠 Fix: Use `dict(TOUR_CHOICES)` to get the tour name properly
            tour_display_name = dict(TOUR_CHOICES).get(
                selected_tour, "Unknown Tour"
            )

            booked_guests = TourBooking.objects.filter(
                tour=selected_tour, date=booking_date, status="confirmed"
            ).aggregate(Sum("guests"))["guests__sum"] or 0

            tour_capacity = TOUR_CAPACITY.get(selected_tour, 0)
            available_slots = tour_capacity - booked_guests

            if guests_requested > available_slots:
                messages.error(
                    request,
                    (
                        f"❌ Sorry, only {available_slots} spots left "
                        f"for {tour_display_name} on {booking_date}."
                    ),
                )
                return redirect("book_tour", tour_slug=selected_tour)

            # ✅ Automatically confirm booking
            booking.status = "confirmed"
            booking.save()
            messages.success(
                request,
                (
                    f"🎉 Your {tour_display_name} booking on "
                    f"{booking_date} is confirmed!"
                ),
            )

            # 🔄 Redirect to success page with booking details
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
