from django.contrib import admin
from django.urls import path
from . import views
from .views import newsletter_signup

urlpatterns = [
    path('', views.index, name='home'),
    path("newsletter-signup/", newsletter_signup, name="newsletter_signup"),
]
