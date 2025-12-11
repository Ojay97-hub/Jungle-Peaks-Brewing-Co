
from django.core.management.base import BaseCommand
from django.conf import settings
import boto3
import os
import mimetypes

class Command(BaseCommand):
    help = 'Uploads missing images from local media to S3 static/images/'

    def handle(self, *args, **options):
        self.stdout.write('Starting upload of missing images...')
        
        # Files identified as missing from S3 but available locally
        files_to_upload = {
            'beer_lovers_gift_basket.png': 'products/beer_lovers_gift_basket.png',
            'craft_beer_sampler_box.png': 'products/craft_beer_sampler_box.png',
            'ultimate_ipa_gift_set.png': 'products/ultimate_ipa_gift_set.png',
            'branded_beer_mug.png': 'products/branded_beer_mug.png',
            'brewery_tote_bag.png': 'products/brewery_tote_bag.png',
            'jungle_peaks_cap.png': 'products/jungle_peaks_cap.png',
            'jungle_peaks_hoodie.png': 'products/jungle_peaks_hoodie.png',
            'jungle_peaks_tshirt.png': 'products/jungle_peaks_tshirt.png',
            'midnight_ridge_porter.png': 'products/midnight_ridge_stout.png', # Note the rename source
            'citrus_cloud_wheat.png': 'products/citrus_cloud_wheat.png',
            'golden_horizon_wheat.png': 'products/golden_horizon_wheat.png',
            'summit_breeze_ipa.png': 'products/summit_breeze_ipa.png',
            'citrus_peak_ipa.png': 'products/citrus_peak_ipa.png',
            'summit_chill.png': 'products/summit_chill.png',
            'crystal_clear.png': 'products/crystal_clear.png',
            'basecamp_lager.png': 'products/basecamp_lager.png',
            'golden_trail_lager.png': 'products/golden_trail_lager.png',
        }

        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        for target_filename, local_source in files_to_upload.items():
            local_path = os.path.join(settings.MEDIA_ROOT, local_source)
            
            if os.path.exists(local_path):
                s3_key = f"static/images/{target_filename}"
                content_type = mimetypes.guess_type(local_path)[0] or 'image/png'
                
                try:
                    self.stdout.write(f'Uploading {target_filename}...')
                    with open(local_path, 'rb') as f:
                        s3.upload_fileobj(
                            f, 
                            settings.AWS_STORAGE_BUCKET_NAME, 
                            s3_key,
                            ExtraArgs={
                                'ContentType': content_type,
                                'ACL': 'public-read',
                                'CacheControl': 'max-age=94608000',
                            }
                        )
                    self.stdout.write(self.style.SUCCESS(f'Successfully uploaded {target_filename}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to upload {target_filename}: {e}'))
            else:
                 self.stdout.write(self.style.WARNING(f'Local file not found: {local_path}'))

        self.stdout.write(self.style.SUCCESS('Upload process completed.'))
