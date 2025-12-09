
from products.models import Product

updates = {
    'Jungle Peaks T-Shirt': 'products/jungle_peaks_tshirt.png',
    'Jungle Peaks Cap': 'products/jungle_peaks_cap.png',
    'Branded Beer Mug': 'products/branded_beer_mug.png',
    'Jungle Peaks Hoodie': 'products/jungle_peaks_hoodie.png',
    'Brewery Tote Bag': 'products/brewery_tote_bag.png',
    'Ultimate IPA Gift Set': 'products/ultimate_ipa_gift_set.png',
    'Craft Beer Sampler Box': 'products/craft_beer_sampler_box.png',
    'Beer Lover\'s Gift Basket': 'products/beer_lovers_gift_basket.png',
    'Dark Peak Stout': 'products/dark_peak_stout.png',
    'Midnight Ridge': 'products/midnight_ridge_stout.png',
    'Shadow Brew': 'products/shadow_brew_porter.png',
    'Velvet Porter': 'products/velvet_porter.png',
    'Canyon Wheat': 'products/canyon_wheat.png',
    'Citrus Cloud Wheat': 'products/citrus_cloud_wheat.png',
    'Golden Horizon': 'products/golden_horizon_wheat.png',
}

with open('update_log_batch.txt', 'w', encoding='utf-8') as f:
    f.write("Starting Batch Update...\n")
    for name, image_path in updates.items():
        try:
            product = Product.objects.get(name=name)
            # Clear conflicting URL
            product.image_url = ''
            # Set new image
            product.image = image_path
            product.save()
            f.write(f"Updated {name}\n")
        except Product.DoesNotExist:
            f.write(f"Product not found: {name}\n")
        except Exception as e:
            f.write(f"Error updating {name}: {e}\n")
    f.write("Batch Update Complete.\n")
