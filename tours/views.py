from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum
from .forms import TourBookingForm
from .models import TourBooking, TOUR_CAPACITY, TOUR_CHOICES
from datetime import date

def tours(request):
    return render(request, 'tours/tours.html')

def book_tour(request, tour_slug=None):
    """Handles tour booking, with an optional pre-selected tour."""
    initial_data = {"tour": tour_slug} if tour_slug else {}

    if request.method == "POST":
        form = TourBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Link the tour booking to the logged-in user
            booking.save()

            # ✅ Check availability dynamically
            selected_tour = booking.tour
            booking_date = booking.date
            guests_requested = booking.guests

            # 🛠 Fix: Use `dict(TOUR_CHOICES)` to get the tour name properly
            tour_display_name = dict(TOUR_CHOICES).get(selected_tour, "Unknown Tour")

            booked_guests = TourBooking.objects.filter(
                tour=selected_tour, date=booking_date, status="confirmed"
            ).aggregate(Sum('guests'))['guests__sum'] or 0

            available_slots = TOUR_CAPACITY.get(selected_tour, 0) - booked_guests

            if guests_requested > available_slots:
                messages.error(
                    request,
                    f"❌ Sorry, only {available_slots} spots left for {tour_display_name} on {booking_date}."
                )
                return redirect("book_tour", tour_slug=selected_tour)  # Reload with error

            # ✅ Automatically confirm booking
            booking.status = "confirmed"
            booking.save()
            messages.success(
                request, f"🎉 Your {tour_display_name} booking on {booking_date} is confirmed!"
            )

            # 🔄 Redirect to success page with booking details
            return redirect("tour_booking_success", booking_id=booking.id)

    else:
        form = TourBookingForm(initial=initial_data)

    return render(request, "tours/book_tour.html", {"form": form})


def tour_booking_success(request, booking_id):
    """ Retrieve specific booking details and display them on the success page. """
    booking = get_object_or_404(TourBooking, id=booking_id)

    return render(request, "tours/tour_booking_success.html", {
        "booking": booking
    })


def check_availability(request):
    """API endpoint to check tour availability in real-time."""
    tour = request.GET.get("tour")
    booking_date = request.GET.get("date")

    if not tour or not booking_date:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    booked_guests = TourBooking.objects.filter(
        tour=tour, date=booking_date, status="confirmed"
    ).aggregate(Sum('guests'))['guests__sum'] or 0

    available_slots = TOUR_CAPACITY[tour] - booked_guests

    return JsonResponse({"available_slots": available_slots})

# edit booking view
@login_required
def edit_booking(request, booking_id):
    """Edit an existing tour booking."""
    booking = get_object_or_404(TourBooking, id=booking_id, user=request.user)  # Ensure user owns the booking
    
    if request.method == "POST":
        form = TourBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Your tour booking has been updated successfully.")
            return redirect("profile")  # Redirect to profile page
    else:
        form = TourBookingForm(instance=booking)  # Pre-fill form with booking data

    return render(request, "tours/edit_booking.html", {"form": form})

# cancel booking view
@login_required
def cancel_booking(request, booking_id):
    """Cancel an existing tour booking."""
    booking = get_object_or_404(TourBooking, id=booking_id, user=request.user)

    # Only allow POST requests for security
    if request.method == "POST":
        booking.delete()
        messages.success(request, "Your tour booking has been successfully canceled.")
    else:
        messages.error(request, "Invalid request method.")

    return redirect("profile")  # Redirect back to profile page

    