from django.shortcuts import get_object_or_404, render, redirect

from taproom.models import Booking 
from .forms import BookingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def taproom(request):
    return render(request, 'taproom/taproom.html')

# Book a table view
@login_required
def booking(request):
    """ Create a taproom booking for the logged-in user. """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Associate the booking with the logged-in user
            booking = form.save(commit=False)
            booking.user = request.user  # Link the booking to the logged-in user
            booking.save()

            messages.success(request, 'Booking has been successfully created.')
            return redirect('booking_success')  # Redirect to booking success page
    else:
        form = BookingForm()

    return render(request, 'taproom/taproom_booking.html', {'form': form})

# booking success view
def booking_success(request):
    return render(request, "taproom/booking_success.html")

# Edit booking view
@login_required
def edit_booking(request, booking_id):
    """Edit an existing taproom booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)  # Ensure user owns the booking
    
    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Your booking has been updated successfully.")
            return redirect("profile")  # Redirect to profile page
    else:
        form = BookingForm(instance=booking)  # Pre-fill the form with booking data

    return render(request, "taproom/edit_booking.html", {"form": form})

# Cancel booking view
@login_required
def cancel_booking(request, booking_id):
    """Cancel an existing taproom booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        booking.delete()  # Remove booking
        messages.success(request, "Your taproom booking has been successfully canceled.")
        return redirect("profile")  # Redirect back to profile page

    return render(request, "taproom/cancel_booking.html", {"booking": booking})