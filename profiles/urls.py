from django.urls import path
from . import views  # Import views from the profiles app
from taproom import views as taproom_views  # Import taproom views correctly
from tours import views as tour_views  # Import tours views correctly

urlpatterns = [
    # Profile page
    path('', views.profile, name='profile'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
    
    # Taproom booking routes
    path('taproom/', taproom_views.taproom, name='taproom'),  # Corrected to use taproom_views
    path('taproom/booking/', taproom_views.booking, name='taproom_booking'),
    path('taproom/booking/success/', taproom_views.booking_success, name='booking_success'),
    
    # Tour booking routes
    path('tours/', tour_views.tours, name='tours'),  # Corrected to use tour_views
    path('tours/book/<slug:tour_slug>/', tour_views.book_tour, name='book_tour'),
    path('tours/booking/success/<int:booking_id>/', tour_views.tour_booking_success, name='tour_booking_success'),
    
    # Reorder route
    path('reorder/<int:order_id>/', views.reorder, name='reorder'),
]