import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile
from tours.models import TourBooking
from taproom.models import Booking


class Order(models.Model):
    """Model representing customer orders."""

    order_number = models.CharField(
        max_length=32, null=False, editable=False
    )
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="orders"
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(
        blank_label="Select a country", null=False, blank=False
    )
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
    )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    original_bag = models.TextField(null=False, blank=False, default="")
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default=""
    )

    def _generate_order_number(self):
        """Generate a random, unique order number using UUID."""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        # Include all line items that have either a product, tour booking, or taproom booking
        self.order_total = (
            self.lineitems.filter(
                models.Q(product__isnull=False) |
                models.Q(tour_booking__isnull=False) |
                models.Q(taproom_booking__isnull=False)
            )
            .aggregate(Sum("lineitem_total"))["lineitem_total__sum"]
            or 0  # Default to 0 if None
        )

        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
            )
        else:
            self.delivery_cost = 0

        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """Model representing individual items in an order."""

    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE,
        related_name="lineitems"
    )
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL
    )
    tour_booking = models.ForeignKey(
        TourBooking, null=True, blank=True, on_delete=models.SET_NULL
    )
    taproom_booking = models.ForeignKey(
        Booking, null=True, blank=True, on_delete=models.SET_NULL
    )
    product_size = models.CharField(
        max_length=2, null=True, blank=True
    )  # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False,
        blank=False, editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        if self.product:
            self.lineitem_total = self.product.price * self.quantity
        elif self.tour_booking:
            self.lineitem_total = self.tour_booking.get_total_price()
        elif self.taproom_booking:
            self.lineitem_total = self.taproom_booking.get_total_price()
        else:
            self.lineitem_total = 0  # Default to 0 if no product, tour, or taproom booking

        super().save(*args, **kwargs)
        # Ensure the order total is updated
        self.order.update_total()

    def __str__(self):
        if self.product:
            return (
                f"SKU {self.product.sku} "
                f"on order {self.order.order_number}"
            )
        elif self.tour_booking:
            return (
                f"Tour {self.tour_booking.get_tour_display()} "
                f"on order {self.order.order_number}"
            )
        elif self.taproom_booking:
            return (
                f"Taproom {self.taproom_booking.get_booking_type_display()} "
                f"on order {self.order.order_number}"
            )
        else:
            return f"Unknown item on order {self.order.order_number}"
