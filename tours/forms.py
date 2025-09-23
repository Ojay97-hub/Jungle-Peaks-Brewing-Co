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
            # For editing, allow users to increase their booking beyond current availability
            # The form validation will handle the actual availability check
            if self.instance and self.instance.pk:
                # This is an edit - allow higher numbers initially
                self.fields["guests"].widget.attrs.update(
                    {
                        "max": max_guests,  # Still limit to capacity
                        "aria-describedby": "guest-help-text",
                    }
                )
                self.fields["guests"].help_text = (
                    f"You currently have {self.instance.guests} attendees. "
                    f"Up to {max_guests} attendees can join this tour."
                )
            else:
                # This is a new booking
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
            # Calculate available slots, excluding current booking if editing
            booking_qs = TourBooking.objects.filter(
                tour=tour, date=booking_date, status="confirmed"
            )
            if self.instance and self.instance.pk:
                # This is an edit - exclude the current booking from count
                booking_qs = booking_qs.exclude(pk=self.instance.pk)

            booked_guests = (
                booking_qs.aggregate(total=Sum("guests")).get("total") or 0
            )
            capacity = TOUR_CAPACITY.get(tour)
            available_slots = max(capacity - booked_guests, 0) if capacity else 0

            tour_name = dict(TOUR_CHOICES).get(tour, "this tour")

            if guests > available_slots:
                if self.instance and self.instance.pk:
                    # This is an edit - provide clearer error message
                    raise forms.ValidationError(
                        (
                            "You can increase your booking to %(available)s attendees "
                            "for %(tour)s on %(date)s. (You currently have %(current)s attendees)"
                        ),
                        params={
                            "available": available_slots,
                            "tour": tour_name,
                            "date": booking_date,
                            "current": self.instance.guests,
                        },
                    )
                else:
                    # This is a new booking
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
