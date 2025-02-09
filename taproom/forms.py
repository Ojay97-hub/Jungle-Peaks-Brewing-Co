from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests', 'special_requests']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'custom-form-control'}),
            'email': forms.EmailInput(attrs={'class': 'custom-form-control'}),
            'phone': forms.TextInput(attrs={'class': 'custom-form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'custom-form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'custom-form-control'}),
            'guests': forms.NumberInput(attrs={'class': 'custom-form-control'}),
            'special_requests': forms.Textarea(attrs={'class': 'custom-form-control', 'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'custom-form-control')