from django.urls import path
from . import views
from .views import booking, cancel_booking, edit_booking

app_name = "taproom"

urlpatterns = [
    path("", views.taproom, name="taproom"),
    path(
        "taproom-booking/", views.booking,
        name="taproom_booking"
    ),
    path(
        "booking-success/", views.booking_success,
        name="booking_success"
    ),
    path(
        "booking/edit/<int:booking_id>/", edit_booking,
        name="edit_booking"
    ),
    path(
        "booking/cancel/<int:booking_id>/", cancel_booking,
        name="cancel_booking"
    ),
    path(
        "api/get-booked-tables/", views.get_booked_tables,
        name="get_booked_tables"
    ),
]
