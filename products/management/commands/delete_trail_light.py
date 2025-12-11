
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Deletes the Trail Light Ale product'

    def handle(self, *args, **options):
        try:
            p = Product.objects.get(name='Trail Light Ale')
            p.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted Trail Light Ale'))
        except Product.DoesNotExist:
            self.stdout.write(self.style.WARNING('Trail Light Ale not found'))
