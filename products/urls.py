from django.contrib import admin
from django.urls import path
from . import views
from .views import add_review, edit_review, delete_review

urlpatterns = [
    path("", views.all_products, name="products"),
    path(
        "<int:product_id>/", views.product_detail,
        name="product_detail"
    ),
    path("add/", views.add_product, name="add_product"),
    path(
        "edit/<int:product_id>/", views.edit_product,
        name="edit_product"
    ),
    path(
        "delete/<int:product_id>/", views.delete_product,
        name="delete_product"
    ),
    path(
        "product/<int:product_id>/add_review/",
        add_review, name="add_review"
    ),
    path(
        "edit-review/<int:review_id>/", edit_review,
        name="edit_review"
    ),
    path(
        "delete-review/<int:review_id>/", delete_review,
        name="delete_review"
    ),
]
