from django.urls import path
from .views import contact_view  # Import the view function

app_name = "contact"

urlpatterns = [
    path("", contact_view, name="contact"),  # This maps "/contact/" to the contact view
]