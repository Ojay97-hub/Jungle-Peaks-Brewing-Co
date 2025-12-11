import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jungle_peaks_brewing.settings')
django.setup()

from products.models import Product

def check_broken_products():
    broken_names = ["Golden Horizon", "Jungle Peaks T-Shirt"]
    
    print(f"AWS Enabled: {settings.USE_AWS}")
    print(f"Media URL: {settings.MEDIA_URL}")
    print("-" * 30)

    for name in broken_names:
        try:
            p = Product.objects.get(name=name)
            print(f"Product: {p.name}")
            print(f"  Image Field: {p.image}")
            print(f"  Image URL Field: {p.image_url}")
            
            # Check if local file exists if mapped to local path
            if p.image:
                local_path = os.path.join(settings.BASE_DIR, 'media', str(p.image))
                exists = os.path.exists(local_path)
                print(f"  Local file path: {local_path}")
                print(f"  Local file exists: {exists}")
        except Product.DoesNotExist:
            print(f"Product not found: {name}")
        except Exception as e:
            print(f"Error checking {name}: {e}")
        print("-" * 30)

if __name__ == "__main__":
    check_broken_products()
