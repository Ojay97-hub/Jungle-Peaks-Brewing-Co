from django.contrib import admin
from .models import TourBooking


@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = ("name", "tour", "date", "guests", "status", "created_at")
    list_filter = ("tour", "date", "status")
    search_fields = ("name", "email")
    ordering = ("-created_at",)
