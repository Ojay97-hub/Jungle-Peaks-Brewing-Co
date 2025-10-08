from django.urls import path
from . import views

app_name = "bag"

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<str:item_id>/', views.add_to_bag, name='add_to_bag'),
    path('adjust/<str:item_id>/', views.adjust_bag, name='adjust_bag'),
    path('remove/<str:item_id>/', views.remove_from_bag, name='remove_from_bag'),
    # Tour-related URLs
    path('add-tour/<str:tour_type>/<str:tour_date>/<int:guests>/', views.add_tour_to_cart, name='add_tour_to_cart'),
    path('remove-tour/<int:cart_item_id>/', views.remove_tour_from_cart, name='remove_tour_from_cart'),
    path('remove-legacy-tour/<str:item_id>/', views.remove_legacy_tour, name='remove_legacy_tour'),
    path('migrate-tours/', views.migrate_tours_to_cart, name='migrate_tours_to_cart'),
    # Taproom-related URLs
    path('add-taproom/<str:booking_type>/<str:booking_date>/<str:booking_time>/', views.add_taproom_to_cart, name='add_taproom_to_cart'),
    path('remove-taproom/<int:cart_item_id>/', views.remove_taproom_from_cart, name='remove_taproom_from_cart'),
]