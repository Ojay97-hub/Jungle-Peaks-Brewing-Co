from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category, Review


class ProductForm(forms.ModelForm):
    """Form for managing product creation and updates."""

    class Meta:
        model = Product
        fields = "__all__"

    image = forms.ImageField(
        label="Image",
        required=False,
        widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        """Customise form fields and set category choices."""
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        category_names = [
            (c.id, c.name) for c in categories
        ]  # Use the `name` field instead of `get_friendly_name`

        self.fields["category"].choices = category_names
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "border-black rounded"


class ReviewForm(forms.ModelForm):
    """Form for submitting product reviews."""

    class Meta:
        model = Review
        fields = ["rating", "comment"]  # Ensure these fields exist in Review
