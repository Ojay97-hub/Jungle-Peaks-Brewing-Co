from django.urls import path
from .views import contact_view  # Import the view function

app_name = "contact"

urlpatterns = [
    # This maps "/contact/" to the contact view
    path("", contact_view, name="contact"),
]
