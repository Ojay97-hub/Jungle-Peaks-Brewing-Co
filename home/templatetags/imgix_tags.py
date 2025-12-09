from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def imgix_url(image_path, params=""):
    """
    Converts an S3 image path into an Imgix-served URL.
    In development, serves from local static or media directories.
    Example:
      {% imgix_url "images/example.jpg" "w=800&h=600&fit=crop" %}
    """
    # In development, serve from local files
    if settings.DEBUG and not getattr(settings, 'USE_AWS', False):
        # Product images are in media/products/
        if image_path.startswith('products/'):
            return f"{settings.MEDIA_URL}{image_path}"
        # Other images (like taproom.jpg) are in static/images/
        else:
            return f"{settings.STATIC_URL}{image_path}"

    # If the path is explicitly a static path (migrated images), serve directly
    if image_path.startswith('/static/'):
        return image_path

    if settings.USE_IMGIX and settings.IMGIX_DOMAIN:
        base_url = f"https://{settings.IMGIX_DOMAIN}/{image_path.lstrip('/')}"
        if params:
            return f"{base_url}?{params}"
        else:
            return base_url

    return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{image_path.lstrip('/')}"

