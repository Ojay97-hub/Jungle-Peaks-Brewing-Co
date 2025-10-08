from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from tours.models import TourBooking
from taproom.models import Booking


class Cart(models.Model):
    """
    Shopping cart model that can handle both products and tours.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    """
    Individual cart item that can be either a product or a tour.
    """
    ITEM_TYPE_CHOICES = [
        ('product', 'Product'),
        ('tour', 'Tour'),
        ('taproom', 'Taproom Booking'),
    ]

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)

    # Product fields (null when item_type is 'tour')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)

    # Tour fields (null when item_type is 'product')
    tour_booking = models.ForeignKey(TourBooking, on_delete=models.CASCADE, null=True, blank=True)
    tour_date = models.DateField(null=True, blank=True)
    tour_guests = models.PositiveIntegerField(null=True, blank=True)

    # Taproom fields (null when item_type is not 'taproom')
    taproom_booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.item_type == 'product':
            return f"{self.product.name} x{self.quantity or 1}"
        elif self.item_type == 'tour':
            return f"Tour booking for {self.tour_booking.tour} on {self.tour_date}"
        elif self.item_type == 'taproom':
            return f"Taproom booking for {self.taproom_booking.name} on {self.taproom_booking.date}"
        else:
            return "Unknown cart item"

    @property
    def price(self):
        """Calculate the total price for this cart item."""
        if self.item_type == 'product':
            base_price = self.product.price
            if self.size:
                # For products with sizes, get the price from the size
                size_obj = self.product.sizes.filter(size=self.size).first()
                if size_obj:
                    base_price = size_obj.price
            return base_price * (self.quantity or 1)
        elif self.item_type == 'tour':
            # Tour pricing - get from the tour booking
            if self.tour_booking:
                return self.tour_booking.get_total_price()
            return 0
        elif self.item_type == 'taproom':
            # Taproom pricing - get from the taproom booking
            if self.taproom_booking:
                return self.taproom_booking.get_total_price()
            return 0
        else:
            return 0

    def save(self, *args, **kwargs):
        """Override save to ensure only one type of item is set."""
        if self.item_type == 'product':
            self.tour_booking = None
            self.tour_date = None
            self.tour_guests = None
            self.taproom_booking = None
        elif self.item_type == 'tour':
            self.product = None
            self.size = None
            self.taproom_booking = None
            # Don't set quantity for tours - leave it null
        elif self.item_type == 'taproom':
            self.product = None
            self.size = None
            self.tour_booking = None
            self.tour_date = None
            self.tour_guests = None
        super().save(*args, **kwargs)
