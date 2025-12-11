from django.core.management.base import BaseCommand
from products.models import Product
from django.conf import settings


class Command(BaseCommand):
    help = 'Fixes all product images to use direct S3 URLs'

    def handle(self, *args, **options):
        self.stdout.write('Starting S3 image fix for ALL products...')
        
        s3_base = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/products"
        
        # Complete mapping of product names to their S3 image filenames
        product_image_map = {
            # Gift Sets
            'Beer Lover\'s Gift Basket': 'beer_lovers_gift_basket.png',
            'Craft Beer Sampler Box': 'craft_beer_sampler_box.png',
            'Ultimate IPA Gift Set': 'ultimate_ipa_gift_set.png',
            
            # Light Beers
            'Alpine Light': 'alpine_light.png',
            'Easy Peak Light': 'easy_peak_light.png',
            'Sunny Days Light Lager': 'sunny_days_light.png',
            'Trail Light Ale': 'trail_ale.png',
            
            # Merchandise
            'Branded Beer Mug': 'branded_beer_mug.png',
            'Brewery Tote Bag': 'brewery_tote_bag.png',
            'Jungle Peaks Cap': 'jungle_peaks_cap.png',
            'Jungle Peaks Hoodie': 'jungle_peaks_hoodie.png',
            'Jungle Peaks T-Shirt': 'jungle_peaks_tshirt.png',
            
            # Pale Ales
            'Amber Glow Pale Ale': 'amber_glow_pale_ale.png',
            'Golden Trail Pale Ale': 'golden_trail_pale_ale.png',
            'Sunrise Pale': 'sunrise_pale_ale.png',
            'Trail Ale': 'trail_ale.png',
            
            # Seasonal Brews
            'Autumn Amber': 'autumn_amber_ale.png',
            'Frosty Peaks Winter Ale': 'frosty_peaks_winter_ale.png',
            'Spring Blossom Ale': 'spring_blossom_ale.png',
            'Summer Breeze': 'summer_breeze_ale.png',
            
            # Sours
            'Berry Burst Sour': 'berry_burst_sour.png',
            'Citrus Zest Sour': 'citrus_zest_sour.png',
            'Passionfruit Pucker': 'passionfruit_pucker_sour.png',
            'Wildflower Sour': 'wildflower_sour.png',
            
            # Stouts & Porters
            'Dark Peak Stout': 'dark_peak_stout.png',
            'Midnight Ridge': 'midnight_ridge_stout.png',
            'Shadow Brew': 'shadow_brew_porter.png',
            'Velvet Porter': 'velvet_porter.png',
            
            # Wheat Beers
            'Canyon Wheat': 'canyon_wheat_beer.png',
            'Citrus Cloud Wheat': 'citrus_cloud_wheat.png',
            'Golden Horizon': 'golden_horizon_wheat.png',
            'Wheat Wanderer': 'wheat_wanderer_beer.png',
            
            # IPAs
            'Summit Breeze IPA': 'summit_breeze_ipa.png',
            'Citrus Peak IPA': 'citrus_peak_ipa.png',
            'Summit Chill': 'summit_chill.png',
            'Crystal Clear': 'crystal_clear.png',
            
            # Lagers
            'Basecamp Lager': 'basecamp_lager.png',
            'Golden Trail Lager': 'golden_trail_lager.png',
            'Kona Light': 'kona_light_700x.jpg',
        }
        
        updated_count = 0
        skipped_count = 0
        not_found_count = 0
        
        products = Product.objects.all()
        
        for product in products:
            if product.name in product_image_map:
                filename = product_image_map[product.name]
                s3_url = f"{s3_base}/{filename}"
                
                # Check if update is needed
                if product.image_url != s3_url:
                    product.image_url = s3_url
                    product.image = None  # Clear image field
                    product.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated {product.name} -> {filename}'))
                    updated_count += 1
                else:
                    self.stdout.write(f'Skipping {product.name} (already correct)')
                    skipped_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'No mapping for: {product.name}'))
                not_found_count += 1
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Finished! Updated: {updated_count}, Skipped: {skipped_count}, No mapping: {not_found_count}'))
