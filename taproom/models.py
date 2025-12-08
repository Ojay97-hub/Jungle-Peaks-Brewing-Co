from django.db import models
from django.contrib.auth.models import User


# Table booking pricing in GBP
TABLE_PRICING = {
    "standard": 10,  # £10 per table booking (base fee)
    "premium": 20,   # £20 per table booking (premium location/time)
}

# Booking a table model
class Booking(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )  # Optional for guests
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)  # End time for reservation duration
    guests = models.PositiveIntegerField()
    table_number = models.IntegerField(null=True, blank=True)
    booking_type = models.CharField(
        max_length=10, choices=[("standard", "Standard"), ("premium", "Premium")], default="standard"
    )
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        """
        Calculate the total price for this table booking.
        """
        return TABLE_PRICING.get(self.booking_type, 0)

    def __str__(self):
        return (
            f"Booking for {self.name} on {self.date} at {self.time}"
        )
