import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jungle_peaks_brewing.settings')
django.setup()

from products.models import Product

IMAGE_MAPPING = {
    # Light Beers
    "Alpine Light": "static/images/alpine_light.png",
    "Easy Peak Light": "static/images/easy_peak_light.png",
    "Sunny Days Light Lager": "static/images/sunny_days_light.png",
    
    # Pale Ales
    "Amber Glow Pale Ale": "static/images/amber_glow_pale_ale.png",
    "Golden Trail Pale Ale": "static/images/golden_trail_pale_ale.png",
    "Sunrise Pale": "static/images/sunrise_pale_ale.png",
    "Trail Ale": "static/images/trail_ale.png",
    
    # Sours
    "Berry Burst Sour": "static/images/berry_burst_sour.png",
    "Wildflower Sour": "static/images/wildflower_sour.png",
    "Passionfruit Pucker": "static/images/passionfruit_pucker_sour.png",
    "Citrus Zest Sour": "static/images/citrus_zest_sour.png",
    
    # Seasonal
    "Summer Breeze": "static/images/summer_breeze_ale.png",
    "Autumn Amber": "static/images/autumn_amber_ale.png",
    "Frosty Peaks Winter Ale": "static/images/frosty_peaks_winter_ale.png",
    "Spring Blossom Ale": "static/images/spring_blossom_ale.png",
    
    # Stouts & Porters
    "Dark Peak Stout": "static/images/dark_peak_stout.png",
    "Midnight Ridge": "static/images/midnight_ridge_porter.png",
    "Shadow Brew": "static/images/shadow_brew_porter.png",
    "Velvet Porter": "static/images/velvet_porter.png",
    
    # Wheat
    "Wheat Wanderer": "static/images/wheat_wanderer_beer.png",
    "Canyon Wheat": "static/images/canyon_wheat_beer.png",
    # Skipped due to quota: Golden Horizon, Citrus Cloud Wheat
}

def update_product_images():
    print("Updating product images...")
    
    updated_count = 0
    from django.conf import settings
    # Assuming custom domain is set in settings, otherwise hardcode or construct it
    # But usually Product.image is a FileField/ImageField. If we set it to a string relative to MEDIA_URL, it strictly expects a file.
    # However, Product model has 'image_url' AND 'image'. Let's check which one is used in templates.
    # Usually 'image' field is preferred. If using S3, we assign the relative path within the bucket.
    
    # Actually, if we just want to update the 'image' field to point to the existing S3 object:
    # We should set product.image.name to the relative path 'static/images/...' 
    # But wait, 'static/images/' is for STATIC files. Media files usually go to 'media/'. 
    # If we uploaded to 'static/images/', we might need to treat them as static or just rely on the path being correct if 'image' field allows it.
    
    # BUT, the Product model has `image = models.ImageField(null=True, blank=True)`.
    # And `image_url = models.URLField(max_length=1024, null=True, blank=True)`.
    
    # If the templates verify generic image_url usage, we can set that. 
    # Let's set both or the most appropriate one. 
    # For now, I will set 'image_url' to the full S3 URL and try to set 'image' name as well.
    
    # Base URL construction:
    base_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/"

    for product_name, s3_path in IMAGE_MAPPING.items():
        try:
            product = Product.objects.get(name=product_name)
            
            # Update image_url
            full_url = base_url + s3_path
            product.image_url = full_url
            
            # For ImageField behavior with S3 backend:
            # We can set the name attribute directly.
            # product.image.name = s3_path 
            # Note: s3_path is "static/images/foo.png".
            # The storage backend might expect "media/..." if default storage is MediaStorage.
            # But we uploaded to "static/images/". 
            # If we set product.image.name = "static/images/foo.png", calling product.image.url will append MEDIA_URL prefix if not careful.
            # But let's check settings again. MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/' where MEDIAFILES_LOCATION = 'media'.
            # So product.image.url would become .../media/static/images/foo.png which is WRONG.
            
            # So we should rely on image_url OR copy items to 'media/' instead of 'static/images/'.
            # OR just use image_url if the template supports it.
            # Most likely the templates check for `product.image` then `product.image_url`.
            
            # Let's just set image_url for now as it's safer given our upload path.
            product.image_url = full_url
             # Clear the image field to ensure image_url is used if the template has fallback logic, 
             # OR if the template prioritizes image field, we might have an issue.
             # Let's assume updating image_url is enough if the 'image' field is empty or if template checks image_url.
            
            product.save()
            print(f"Updated {product_name} -> {full_url}")
            updated_count += 1
            
        except Product.DoesNotExist:
            print(f"Product not found: {product_name}")
        except Exception as e:
            print(f"Error updating {product_name}: {e}")

    print(f"Finished. Updated {updated_count} products.")

if __name__ == "__main__":
    update_product_images()
