from django.shortcuts import render, redirect 
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