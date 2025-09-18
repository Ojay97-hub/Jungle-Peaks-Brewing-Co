from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from .forms import TourBookingForm
from .models import TOUR_CAPACITY, TourBooking


class TourBookingUpdateTests(TestCase):
    """Regression tests for booking updates and capacity handling."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="tourist", email="tourist@example.com", password="password123"
        )
        self.booking_date = date.today() + timedelta(days=7)
        self.booking = TourBooking.objects.create(
            user=self.user,
            tour="guided",
            name="Primary Guest",
            email="tourist@example.com",
            phone="123456789",
            date=self.booking_date,
            guests=10,
            status="confirmed",
        )
        # Companion booking to reserve additional capacity on the same tour/date
        self.other_booking = TourBooking.objects.create(
            user=self.user,
            tour="guided",
            name="Secondary Guest",
            email="other@example.com",
            phone="987654321",
            date=self.booking_date,
            guests=5,
            status="confirmed",
        )

    def _get_form(self, guests):
        """Helper to build a form for the existing booking."""
        form_data = {
            "tour": self.booking.tour,
            "name": self.booking.name,
            "email": self.booking.email,
            "phone": self.booking.phone,
            "date": self.booking.date,
            "guests": guests,
            "special_requests": self.booking.special_requests,
        }
        return TourBookingForm(data=form_data, instance=self.booking)

    def test_can_reduce_guests_without_validation_error(self):
        """Users should be able to reduce their guest count."""
        form = self._get_form(guests=8)
        self.assertTrue(form.is_valid(), form.errors.as_text())
        updated_booking = form.save()
        self.assertEqual(updated_booking.guests, 8)
        self.assertEqual(updated_booking.status, "confirmed")

    def test_can_increase_guests_within_remaining_capacity(self):
        """Increasing guests is permitted while respecting the limit."""
        form = self._get_form(guests=12)
        self.assertTrue(form.is_valid(), form.errors.as_text())
        updated_booking = form.save()
        self.assertEqual(updated_booking.guests, 12)

    def test_rejects_guest_numbers_above_capacity(self):
        """Validation should prevent overbooking scenarios."""
        form = self._get_form(guests=16)
        self.assertFalse(form.is_valid())
        self.assertIn("Only", form.errors.get("__all__")[0])

    def test_rejects_zero_guests(self):
        """The guest field enforces a positive number."""
        form = self._get_form(guests=0)
        self.assertFalse(form.is_valid())
        self.assertIn("guests", form.errors)

    def test_allows_booking_up_to_remaining_capacity(self):
        """Edge case where requested guests equals the remaining capacity."""
        remaining_capacity = TOUR_CAPACITY[self.booking.tour] - self.other_booking.guests
        form = self._get_form(guests=remaining_capacity)
        self.assertTrue(form.is_valid(), form.errors.as_text())

    def test_model_save_still_prevents_manual_overbooking(self):
        """Direct model usage should mirror form validation."""
        self.booking.guests = TOUR_CAPACITY[self.booking.tour] + 1
        with self.assertRaises(ValueError):
            self.booking.save()
