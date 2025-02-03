from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import TourBooking

class TourBookingForm(forms.ModelForm):
    class Meta:
        model = TourBooking
        fields = ['tour', 'name', 'email', 'phone', 'date', 'guests', 'special_requests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'tour': forms.Select(attrs={'class': 'form-select'}),  # Dropdown styling
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'booking-form'  # ✅ Custom class to target this form only
        self.helper.label_class = 'fw-bold'  # Bold labels
        self.helper.field_class = 'mb-3'  # Add spacing between fields
        self.helper.add_input(Submit('submit', 'Confirm Booking', css_class='btn btn-primary btn-lg shadow-sm'))
