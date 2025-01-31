from django.urls import path
from . import views

urlpatterns = [
    path('', views.taproom, name='taproom'),
]
