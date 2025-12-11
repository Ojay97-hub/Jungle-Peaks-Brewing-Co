import os
import django
import boto3
from django.conf import settings
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jungle_peaks_brewing.settings')
django.setup()

def upload_file(file_path, s3_name):
    print(f"Uploading {file_path} to {s3_name}...")
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    try:
        with open(file_path, 'rb') as data:
            s3.upload_fileobj(
                data, 
                settings.AWS_STORAGE_BUCKET_NAME, 
                s3_name, # Expecting full relative path now
                ExtraArgs={'ContentType': 'image/png', 'ACL': 'public-read'}
            )
        print(f"Success! URL: https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_name}")
    except Exception as e:
        print(f"Error uploading {s3_name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python upload_to_s3.py <local_path> <s3_key_path>")
    else:
        upload_file(sys.argv[1], sys.argv[2])
