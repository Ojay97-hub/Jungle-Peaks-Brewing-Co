from django.urls import path
from . import views
from .views import booking


urlpatterns = [
    path('', views.taproom, name='taproom'),
     path("taproom-booking/", views.booking, name="taproom_booking"),
    path("booking-success/", views.booking_success, name="booking_success"),
]
