from django.contrib import admin
from django.contrib import messages
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin configuration for Booking model."""

    list_display = (
        "name", "email", "phone", "date",
        "time", "guests", "table_number", "booking_type", "status", "created_at"
    )
    list_filter = ("date", "time", "guests", "status", "booking_type")
    search_fields = ("name", "email", "phone")
    ordering = ("-created_at",)
    actions = ["confirm_bookings", "decline_bookings"]

    @admin.action(description="Confirm selected bookings")
    def confirm_bookings(self, request, queryset):
        """Action to bulk confirm selected bookings."""
        updated = queryset.update(status="confirmed")
        self.message_user(
            request,
            f"{updated} booking(s) successfully confirmed.",
            messages.SUCCESS
        )

    @admin.action(description="Decline selected bookings")
    def decline_bookings(self, request, queryset):
        """Action to bulk decline selected bookings."""
        updated = queryset.update(status="declined")
        self.message_user(
            request,
            f"{updated} booking(s) declined.",
            messages.WARNING
        )

