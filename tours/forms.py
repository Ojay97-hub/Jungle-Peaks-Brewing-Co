from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import TourBooking, TOUR_CAPACITY, TOUR_CHOICES
from django.db.models import Sum
from datetime import date


class TourBookingForm(forms.ModelForm):
    """Form for booking a tour with validation."""

    class Meta:
        model = TourBooking
        fields = [
            "tour", "name", "email", "phone", "date",
            "guests", "special_requests"
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "autocomplete": "name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "autocomplete": "email"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "autocomplete": "tel"}
            ),
            "date": forms.DateInput(
                attrs={"type": "date", "class": "form-control",
                       "autocomplete": "off"}
            ),
            "guests": forms.NumberInput(
                attrs={"class": "form-control", "min": 1,
                       "autocomplete": "off"}
            ),
            "special_requests": forms.Textarea(
                attrs={"class": "form-control", "rows": 3,
                       "autocomplete": "off"}
            ),
            "tour": forms.Select(
                attrs={"class": "form-select", "autocomplete": "off"}
            ),
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form with crispy forms styling and guest limits."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "booking-form"
        self.helper.label_class = "fw-bold"
        self.helper.field_class = "mb-3"
        self.helper.add_input(
            Submit("submit", "Confirm Booking",
                   css_class="btn btn-primary btn-lg shadow-sm")
        )

        selected_tour = None
        if "initial" in kwargs and kwargs["initial"].get("tour"):
            selected_tour = kwargs["initial"]["tour"]
        elif self.instance and self.instance.tour:
            selected_tour = self.instance.tour

        if selected_tour:
            max_guests = TOUR_CAPACITY.get(selected_tour, 20)
            self.fields["guests"].widget.attrs.update(
                {
                    "max": max_guests,
                    "aria-describedby": "guest-help-text",
                }
            )
            self.fields["guests"].help_text = (
                f"Up to {max_guests} attendees can join this tour."
            )

    def clean_date(self):
        """Ensure the user selects a future date."""
        booking_date = self.cleaned_data.get("date")
        if booking_date and booking_date < date.today():
            raise forms.ValidationError("You cannot book a tour in the past.")
        return booking_date

    def clean(self):
        """Validate guest count based on availability."""
        cleaned_data = super().clean()
        tour = cleaned_data.get("tour")
        booking_date = cleaned_data.get("date")
        guests = cleaned_data.get("guests")

        if guests is not None and guests < 1:
            self.add_error(
                "guests",
                "Please choose at least one attendee.",
            )
            return cleaned_data

        if tour and booking_date and guests is not None:
            booking_qs = TourBooking.objects.filter(
                tour=tour, date=booking_date, status="confirmed"
            )
            if self.instance.pk:
                booking_qs = booking_qs.exclude(pk=self.instance.pk)

            booked_guests = (
                booking_qs.aggregate(total=Sum("guests")).get("total") or 0
            )
            capacity = TOUR_CAPACITY.get(tour)
            available_slots = max(capacity - booked_guests, 0) if capacity else 0

            tour_name = dict(TOUR_CHOICES).get(tour, "this tour")

            if guests > available_slots:
                raise forms.ValidationError(
                    (
                        "Only %(available)s attendees can be booked for "
                        "%(tour)s on %(date)s."
                    ),
                    params={
                        "available": available_slots,
                        "tour": tour_name,
                        "date": booking_date,
                    },
                )

        return cleaned_data
