import os
import django
import boto3
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jungle_peaks_brewing.settings')
django.setup()

def list_static_contents():
    print(f"Checking bucket: {settings.AWS_STORAGE_BUCKET_NAME}")
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    try:
        response = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix='static/css/')
        if 'Contents' in response:
            print("Found CSS files in S3:")
            for obj in response['Contents']:
                print(f"- {obj['Key']} (LastModified: {obj['LastModified']})")
        else:
            print("No CSS files found in 'static/css/'.")
            
    except Exception as e:
        print(f"Error accessing S3: {e}")

if __name__ == "__main__":
    list_static_contents()
