from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Form for handling contact messages."""

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]

        # Optional: add custom widgets or labels
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Enter your name"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Enter your email"}
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Write your message here..."
                }
            ),
        }
