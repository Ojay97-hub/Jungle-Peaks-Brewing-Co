
from products.models import Product

products_to_fix = [
    'Citrus Peak IPA',
    'Summit Breeze IPA',
    'Golden Trail Lager',
    'Crystal Clear',
    'Basecamp Lager',
    'Summit Chill'
]

with open('clear_urls_log.txt', 'w', encoding='utf-8') as f:
    f.write("Clearing image_url for updated products...\n")
    for name in products_to_fix:
        try:
            product = Product.objects.get(name=name)
            # Clear the image_url field so the template uses the 'image' field instead
            old_url = product.image_url
            product.image_url = '' 
            product.save()
            f.write(f"Cleared image_url for {name} (was: {old_url})\n")
        except Product.DoesNotExist:
            f.write(f"Product not found: {name}\n")
        except Exception as e:
            f.write(f"Error updating {name}: {e}\n")
    f.write("Done.\n")
