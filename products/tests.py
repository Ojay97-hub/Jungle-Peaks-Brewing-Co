import shutil
import tempfile
from pathlib import Path

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Category, Product


class ProductImageUploadTests(TestCase):
    """Tests covering product creation edge cases and image uploads."""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.category = Category.objects.create(
            name="Tasters", description="Sample beverages"
        )

    def _get_valid_payload(self):
        return {
            "name": "Sample Product",
            "sku": "SKU12345",
            "type": "Drink",
            "description": "Tasting flight",
            "category": str(self.category.id),
            "price": "9.99",
            "image_url": "",
            "abv": "",
            "rating": "",
        }

    def test_add_product_persists_uploaded_image(self):
        """The uploaded image should be stored and linked to the product."""
        self.client.login(username="admin", password="adminpass")
        payload = self._get_valid_payload()
        image_content = SimpleUploadedFile(
            "test-image.gif",
            content=(
                b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
                b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00"
                b"\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
            ),
            content_type="image/gif",
        )
        payload["image"] = image_content

        media_root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(media_root, ignore_errors=True))
        with override_settings(
            MEDIA_ROOT=media_root,
            DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage",
        ):
            response = self.client.post(
                reverse("add_product"), payload, follow=True
            )
        self.assertEqual(response.status_code, 200)
        product = Product.objects.get(sku="SKU12345")
        self.assertTrue(product.image, "Uploaded image should be attached to the product")
        self.assertTrue(
            Path(product.image.path).exists(),
            "Image file should exist in the configured media directory",
        )

    @override_settings(AWS_STORAGE_BUCKET_NAME="test-bucket")
    def test_product_detail_uses_fallback_image(self):
        """Products without an uploaded image render the shared placeholder."""
        product = Product.objects.create(
            name="No Image",
            sku="NOIMG",
            type="Merch",
            description="No image available",
            category=self.category,
            price=5,
        )
        response = self.client.get(reverse("product_detail", args=[product.id]))
        self.assertContains(response, "noimage.png")

    def test_validation_errors_are_displayed_on_create(self):
        """Invalid submissions should surface helpful errors to the user."""
        self.client.login(username="admin", password="adminpass")
        payload = self._get_valid_payload()
        payload.pop("name")  # Force a validation error

        response = self.client.post(reverse("add_product"), payload)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
