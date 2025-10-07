from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Available tour options with descriptions and duration
TOUR_CHOICES = [
    ("guided", "Guided Brewery Tour"),
    ("sunset", "Sunset Tour"),
    ("craft_tasting", "Craft Beer Tasting"),
    ("seasonal", "Seasonal Selection"),
    ("brewer_session", "Master Brewer's Session"),
]

# Maximum guest limits for each tour
TOUR_CAPACITY = {
    "guided": 20,
    "sunset": 15,
    "craft_tasting": 25,
    "seasonal": 10,
    "brewer_session": 8,
}

# Tour duration in minutes
TOUR_DURATION = {
    "guided": 90,
    "sunset": 120,
    "craft_tasting": 75,
    "seasonal": 100,
    "brewer_session": 180,
}

# Tour pricing in GBP
TOUR_PRICING = {
    "guided": 25,  # £25 per person
    "sunset": 35,  # £35 per person (premium experience)
    "craft_tasting": 20,  # £20 per person
    "seasonal": 28,  # £28 per person
    "brewer_session": 45,  # £45 per person (expert-led)
}

# Booking status choices
BOOKING_STATUS = [
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("canceled", "Canceled"),
]


class TourBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True)  # Optional for guests
    tour = models.CharField(max_length=20, choices=TOUR_CHOICES)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10,
                              choices=BOOKING_STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_tour_display()} on {self.date}"

    def get_available_slots(self):
        """
        Return the remaining capacity for the selected tour and date.

        When a booking is being updated we need to exclude the current
        instance from the calculation so that guests can be reduced without
        triggering the overbooking check. This mirrors the validation that
        happens in the form layer and keeps the model logic robust when it is
        used directly in tests or Django admin updates.
        """
        booking_filter = TourBooking.objects.filter(
            tour=self.tour, date=self.date, status="confirmed"
        )
        if self.pk:
            booking_filter = booking_filter.exclude(pk=self.pk)

        booked_guests = (
            booking_filter.aggregate(total=models.Sum("guests")).get("total")
            or 0
        )
        capacity = TOUR_CAPACITY.get(self.tour, 0)
        return capacity - booked_guests

    def get_total_price(self):
        """
        Calculate the total price for this tour booking.
        Price per person * number of guests.
        """
        price_per_person = TOUR_PRICING.get(self.tour, 0)
        return price_per_person * self.guests

    def get_price_per_person(self):
        """
        Get the price per person for this tour.
        """
        return TOUR_PRICING.get(self.tour, 0)

    def save(self, *args, **kwargs):
        """ Prevent overbooking """
        if self.guests > self.get_available_slots():
            raise ValueError("Not enough slots available for this tour.")
        super().save(*args, **kwargs)
