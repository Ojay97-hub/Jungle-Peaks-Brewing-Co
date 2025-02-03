from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TourBookingForm
from .models import TourBooking

# Create your views here.
def tours(request):
    return render(request, 'tours/tours.html')

def book_tour(request, tour_slug=None):
    """Handles tour booking, with an optional pre-selected tour."""
    if request.method == "POST":
        form = TourBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your tour has been booked successfully!")
            return redirect("tour_booking_success")
    else:
        initial_data = {"tour": tour_slug} if tour_slug else {}
        form = TourBookingForm(initial=initial_data)

    return render(request, "tours/book_tour.html", {"form": form})

def tour_booking_success(request):
    """ Retrieve the latest booking details and display them on the success page. """
    latest_booking = TourBooking.objects.latest('created_at')  # Fetch the most recent booking

    return render(request, "tours/tour_booking_success.html", {
        "booking": latest_booking
    })