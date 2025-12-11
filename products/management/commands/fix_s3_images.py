from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Fixes broken S3 images for specific products by setting direct S3 URLs'

    def handle(self, *args, **options):
        # Product mapping: Name -> S3 URL
        updates = {
            'Jungle Peaks T-Shirt': 'https://jungle-peaks-brewing.s3.amazonaws.com/media/products/jungle_peaks_tshirt.png',
            'Golden Horizon': 'https://jungle-peaks-brewing.s3.amazonaws.com/media/products/golden_horizon_wheat.png'
        }

        self.stdout.write('Starting image fix...')

        for name, url in updates.items():
            try:
                product = Product.objects.get(name=name)
                
                # Check if update is needed
                if product.image_url != url:
                    product.image_url = url
                    product.image = None  # Clear the image field to avoid conflicts
                    product.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated {name}'))
                else:
                    self.stdout.write(f'Skipping {name} (already updated)')
                    
            except Product.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Product not found: {name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error updating {name}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Finished fixing images'))
