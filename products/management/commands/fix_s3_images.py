from django.core.management.base import BaseCommand
from products.models import Product
from django.conf import settings


class Command(BaseCommand):
    help = 'Fixes all product images to use direct S3 URLs instead of Imgix'

    def handle(self, *args, **options):
        self.stdout.write('Starting S3 image migration for ALL products...')
        
        products = Product.objects.all()
        updated_count = 0
        skipped_count = 0
        
        s3_base = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/products"
        
        for product in products:
            # Skip if already has a valid S3 URL in image_url
            if product.image_url and 's3.amazonaws.com' in product.image_url:
                self.stdout.write(f'Skipping {product.name} (already using S3 URL)')
                skipped_count += 1
                continue
            
            # If product has an image field set, convert it to S3 URL
            if product.image:
                # Extract filename from the image field
                image_name = str(product.image).split('/')[-1]
                s3_url = f"{s3_base}/{image_name}"
                
                product.image_url = s3_url
                product.image = None  # Clear image field to avoid Imgix routing
                product.save()
                
                self.stdout.write(self.style.SUCCESS(f'Updated {product.name} -> {s3_url}'))
                updated_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'Skipping {product.name} (no image field set)'))
                skipped_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Finished! Updated: {updated_count}, Skipped: {skipped_count}'))
