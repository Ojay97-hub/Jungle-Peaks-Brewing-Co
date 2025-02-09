from django.urls import path
from . import views
from .views import book_tour, tour_booking_success

urlpatterns = [
    path('', views.tours, name='tours'),
    path("book/", book_tour, name="book_tour"),
    path("book/<str:tour_slug>/", book_tour, name="book_tour_specific"),
    path("booking-success/", tour_booking_success, name="tour_booking_success"),
    path("tours/success/<int:booking_id>/", views.tour_booking_success, name="tour_booking_success"),
    path("check-availability/", views.check_availability, name="check_availability"),
]