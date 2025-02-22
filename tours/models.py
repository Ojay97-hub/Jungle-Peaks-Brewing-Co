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
        """ Returns the number of available slots for
            the selected tour on a given date. """
        booked_guests = (
                    TourBooking.objects
                    .filter(tour=self.tour, date=self.date, status="confirmed")
                    .aggregate(total=models.Sum("guests"))
                    .get("total", 0) or 0
                )
        return TOUR_CAPACITY[self.tour] - booked_guests

    def save(self, *args, **kwargs):
        """ Prevent overbooking """
        if self.guests > self.get_available_slots():
            raise ValueError("Not enough slots available for this tour.")
        super().save(*args, **kwargs)
