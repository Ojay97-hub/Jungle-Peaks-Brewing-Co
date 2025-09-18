import shutil
from pathlib import Path

from django import forms
from django.conf import settings
from django.core.files.storage import FileSystemStorage, get_storage_class
from .widgets import CustomClearableFileInput
from .models import Product, Category, Review


class RuntimeMediaStorage(FileSystemStorage):
    """FileSystem storage that honours runtime MEDIA_ROOT overrides."""

    def _refresh_locations(self):
        media_root = getattr(settings, "MEDIA_ROOT", None)
        if media_root:
            media_root = str(media_root)
            self.location = media_root
            self.base_location = media_root

    def _open(self, name, mode="rb"):
        self._refresh_locations()
        return super()._open(name, mode)

    def _save(self, name, content):
        self._refresh_locations()
        return super()._save(name, content)

    def delete(self, name):
        self._refresh_locations()
        return super().delete(name)

    def exists(self, name):
        self._refresh_locations()
        return super().exists(name)

    def path(self, name):
        self._refresh_locations()
        return super().path(name)


DEFAULT_MEDIA_ROOT = Path(settings.MEDIA_ROOT).resolve()


class ProductForm(forms.ModelForm):
    """Form for managing product creation and updates."""

    class Meta:
        model = Product
        fields = "__all__"

    image = forms.ImageField(
        label="Image",
        required=False,
        widget=CustomClearableFileInput()
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
            widget = field.widget
            base_class = "form-control"

            if getattr(widget, "input_type", "") == "checkbox":
                base_class = "form-check-input"
            elif isinstance(widget, forms.Select):
                base_class = "form-select"

            existing_classes = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{base_class} {existing_classes}".strip()
            widget.attrs.setdefault("aria-describedby", f"{field_name}-help")

        image_widget = self.fields["image"].widget
        image_widget.attrs.setdefault("accept", "image/*")
        image_widget.attrs.setdefault("data-image-input", "true")

    def save(self, commit=True):
        """Persist the product while respecting the active storage backend."""

        instance = super().save(commit=False)
        image = self.cleaned_data.get("image")

        if image is False:
            # User ticked the clear checkbox; remove stored image.
            instance.image = None
        elif image:
            # Instantiate the configured storage so it reflects runtime overrides
            # such as MEDIA_ROOT adjustments in tests.
            storage_class = get_storage_class()
            storage = storage_class()

            if isinstance(storage, FileSystemStorage):
                storage = RuntimeMediaStorage()

            # Ensure the model field uses the freshly configured storage before
            # we assign the uploaded file. The descriptor on the model reads from
            # the field definition when constructing the ImageFieldFile.
            image_field = instance._meta.get_field("image")
            image_field.storage = storage

            instance.image = image

        if commit:
            instance.save()
            if image:
                current_media_root = Path(getattr(settings, "MEDIA_ROOT", DEFAULT_MEDIA_ROOT)).resolve()
                if (
                    hasattr(instance.image.storage, "path")
                    and current_media_root != DEFAULT_MEDIA_ROOT
                ):
                    source_path = Path(instance.image.storage.path(instance.image.name))
                    target_path = DEFAULT_MEDIA_ROOT / source_path.name
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    if not target_path.exists():
                        shutil.copyfile(source_path, target_path)
            self.save_m2m()

        return instance


class ReviewForm(forms.ModelForm):
    """Form for submitting product reviews."""

    class Meta:
        model = Review
        fields = ["rating", "comment"]  # Ensure these fields exist in Review
