import os
import django
import boto3
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jungle_peaks_brewing.settings')
django.setup()

def list_s3_contents():
    print(f"Checking bucket: {settings.AWS_STORAGE_BUCKET_NAME}")
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    try:
        response = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix='static/images/')
        if 'Contents' in response:
            print("Successfully accessed S3. Found objects:")
            for obj in response['Contents']:
                print(f"- {obj['Key']}")
        else:
            print("Successfully accessed S3. No objects found in 'static/images/'.")
            
    except Exception as e:
        print(f"Error accessing S3: {e}")

if __name__ == "__main__":
    list_s3_contents()
