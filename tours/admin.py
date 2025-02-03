from django.contrib import admin
from .models import TourBooking

@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'tour', 'date', 'guests', 'created_at')  # ✅ Columns to display
    list_filter = ('tour', 'date')  # ✅ Add filtering by tour and date
    search_fields = ('name', 'email', 'phone')  # ✅ Enable search functionality
    ordering = ('-created_at',)  # ✅ Show latest bookings first
