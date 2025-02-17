from django.urls import path
from .views import contact  # Import the view function

# Set the namespace for this app
app_name = "contact"

urlpatterns = [
    path("", contact, name="contact"),  # This maps "/contact/" to the contact view
]