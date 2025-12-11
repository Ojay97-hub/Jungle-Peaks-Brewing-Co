from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Debug product image data'

    def handle(self, *args, **options):
        products = Product.objects.all()
        
        for product in products:
            self.stdout.write(f'{product.name}:')
            self.stdout.write(f'  image: {product.image if product.image else "EMPTY"}')
            self.stdout.write(f'  image_url: {product.image_url if product.image_url else "EMPTY"}')
            self.stdout.write('')
