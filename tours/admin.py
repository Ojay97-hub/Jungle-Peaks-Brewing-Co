from django.contrib import admin
from django.contrib import messages
from .models import TourBooking


@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = ("name", "tour", "date", "guests", "status", "created_at")
    list_filter = ("tour", "date", "status")
    search_fields = ("name", "email")
    ordering = ("-created_at",)
    actions = ["confirm_bookings"]

    @admin.action(description="Confirm selected bookings")
    def confirm_bookings(self, request, queryset):
        """
        Action to bulk confirm selected bookings.
        """
        updated = queryset.update(status="confirmed")
        self.message_user(
            request,
            f"{updated} booking(s) successfully confirmed.",
            messages.SUCCESS
        )
