from django.shortcuts import render, redirect 
from .forms import BookingForm
from django.contrib import messages

# Create your views here.
def taproom(request):
    return render(request, 'taproom/taproom.html')

# Book a table view
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking has been successfully created.')
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'taproom/booking.html', {'form': form})

# booking success view
def booking_success(request):
    return render(request, "taproom/booking_success.html")