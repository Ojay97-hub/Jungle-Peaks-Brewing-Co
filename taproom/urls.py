from django.urls import path
from . import views
from .views import booking


urlpatterns = [
    path('', views.taproom, name='taproom'),
    path("booking/", views.booking, name="booking"), 
    path("booking-success/", views.booking_success, name="booking_success"),
]
