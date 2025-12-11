
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Deletes products that are not in the valid local ID set'

    def handle(self, *args, **options):
        # Valid IDs from local DB (as of the recent dump)
        valid_ids = [1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
        
        self.stdout.write(f'Checking for products not in list: {valid_ids}')
        
        products_to_delete = Product.objects.exclude(id__in=valid_ids)
        count = products_to_delete.count()
        
        if count > 0:
            self.stdout.write(self.style.WARNING(f'Found {count} products to delete.'))
            for product in products_to_delete:
                self.stdout.write(f'- Deleting: {product.name} (ID: {product.id})')
            
            deleted_count, _ = products_to_delete.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} products.'))
        else:
            self.stdout.write(self.style.SUCCESS('No extra products found. Sync is complete.'))
