
from django.core.management.base import BaseCommand
from django.conf import settings
import urllib.request
import urllib.error

class Command(BaseCommand):
    help = 'Validates that the images in the map actually exist on S3'

    def handle(self, *args, **options):
        self.stdout.write('Checking S3 image availability...')
        
        s3_base = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/images"
        
        # Same map as in fix_s3_images.py
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
        
        missing = []
        found = []
        
        for name, filename in product_image_map.items():
            url = f"{s3_base}/{filename}"
            try:
                request = urllib.request.Request(url, method='HEAD')
                with urllib.request.urlopen(request) as response:
                    if response.status == 200:
                        self.stdout.write(self.style.SUCCESS(f'[OK] {filename}'))
                        found.append(filename)
            except urllib.error.HTTPError as e:
                self.stdout.write(self.style.ERROR(f'[FAIL] {filename} - {e.code}'))
                missing.append(filename)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[ERR] {filename} - {e}'))
                missing.append(filename)

        self.stdout.write('\nSummary:')
        self.stdout.write(self.style.SUCCESS(f'Found: {len(found)}'))
        self.stdout.write(self.style.ERROR(f'Missing: {len(missing)}'))
        
        if missing:
            self.stdout.write('\nMissing Files:')
            for f in missing:
                self.stdout.write(f"- {f}")
