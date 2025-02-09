from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import TourBooking, TOUR_CAPACITY, TOUR_CHOICES
from django.db.models import Sum
from datetime import date

class TourBookingForm(forms.ModelForm):
    class Meta:
        model = TourBooking
        fields = ['tour', 'name', 'email', 'phone', 'date', 'guests', 'special_requests']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'tel'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'autocomplete': 'off'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'autocomplete': 'off'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'autocomplete': 'off'}),
            'tour': forms.Select(attrs={'class': 'form-select', 'autocomplete': 'off'}),  
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'booking-form'  
        self.helper.label_class = 'fw-bold'  
        self.helper.field_class = 'mb-3'  
        self.helper.add_input(Submit('submit', 'Confirm Booking', css_class='btn btn-primary btn-lg shadow-sm'))

        if 'initial' in kwargs and 'tour' in kwargs['initial']:
            self.fields['guests'].widget.attrs['max'] = TOUR_CAPACITY.get(kwargs['initial']['tour'], 20)

    def clean_date(self):
        """ Ensure the user selects a future date. """
        booking_date = self.cleaned_data.get('date')
        if booking_date and booking_date < date.today():
            raise forms.ValidationError("You cannot book a tour in the past.")
        return booking_date

    def clean(self):
        """ Validate guest count based on availability. """
        cleaned_data = super().clean()
        tour = cleaned_data.get('tour')
        booking_date = cleaned_data.get('date')
        guests = cleaned_data.get('guests')

        if tour and booking_date:
            booked_guests = TourBooking.objects.filter(
                tour=tour, date=booking_date, status="confirmed"
            ).aggregate(Sum('guests'))['guests__sum'] or 0
            available_slots = TOUR_CAPACITY[tour] - booked_guests

            # ✅ FIXED: Use TOUR_CHOICES correctly
            tour_name = dict(TOUR_CHOICES).get(tour, "this tour")
            if guests > available_slots:
                raise forms.ValidationError(
                    f"Only {available_slots} spots are available for {tour_name} on {booking_date}."
                )

        return cleaned_data