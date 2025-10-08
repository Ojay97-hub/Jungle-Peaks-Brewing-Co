from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def imgix_url(image_path, params=""):
    """
    Converts an S3 image path into an Imgix-served URL.
    Example:
      {% imgix_url "images/example.jpg" "w=800&h=600&fit=crop" %}
    """
    if settings.USE_IMGIX and settings.IMGIX_DOMAIN:
        base_url = f"https://{settings.IMGIX_DOMAIN}/{image_path.lstrip('/')}"
        if params:
            return f"{base_url}?{params}"
        else:
            return base_url

    return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{image_path.lstrip('/')}"
