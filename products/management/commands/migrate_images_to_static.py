from django.core.management.base import BaseCommand
from products.models import Product
import os

class Command(BaseCommand):
    help = 'Migrate product images from media to static URLs'

    def handle(self, *args, **kwargs):
        # List of known generated images mapping (filename -> static path)
        # We assume the file name in media matches the intended static file name
        
        products = Product.objects.all()
        updated_count = 0
        
        for product in products:
            # Check if product has an image assigned in the DB (even if file is missing in S3)
            # OR if we can match it by name/slug to one of our known files
            
            # Simplified matching logic based on what we saw in the directory list
            possible_filename = product.name.lower().replace(' ', '_').replace("'", "").replace("-", "_") + ".png"
            
            # Check if this file exists in our new static directory
            # In a real deployment, we check if the static URL is valid, but here we'll just assign it
            # assuming we just moved them.
            
            static_path = f"products/images/{possible_filename}"
            
            # We will use the 'image_url' field for static paths to avoid FileField storage issues on Heroku
            # The static path needs to be prefixed with the STATIC_URL in the template, 
            # OR we can store the full rooted relative path if we know it.
            # Best practice: Store the relative path and let template resolve it, 
            # BUT your template logic falls back to image_url being a full URL.
            
            # Let's set it to a relative path that we can easily use with the 'static' tag in templates,
            # or just a direct path assuming STATIC_URL is /static/
            
            # Actually, the cleanest way is often to just clear the FileField (since it's broken on Heroku without S3)
            # and set image_url to the static path.
            
            # We'll use a hardcoded assumption that we moved the files to static/products/images/
            full_static_url = f"/static/products/images/{possible_filename}"
            
            # Check if we have this file locally to confirm we should update
            local_static_path = os.path.join("products", "static", "products", "images", possible_filename)
            
            if os.path.exists(local_static_path):
                self.stdout.write(f"Found static image for {product.name}: {possible_filename}")
                
                # Update database
                product.image = None # Clear the file field to avoid 404 access errors
                product.image_url = full_static_url
                product.save()
                updated_count += 1
            else:
                self.stdout.write(self.style.WARNING(f"No matching static image found for {product.name} (looked for {possible_filename})"))

        self.stdout.write(self.style.SUCCESS(f"Successfully updated {updated_count} products to use static images"))
