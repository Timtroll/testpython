import boto3
from botocore.exceptions import NoCredentialsError

s3_client = boto3.client('s3', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')

BUCKET_NAME = 'your-bucket-name'

def upload_file_to_s3(file_name, object_name=None):
    try:
        s3_client.upload_file(file_name, BUCKET_NAME, object_name or file_name)
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{object_name or file_name}"
    except NoCredentialsError:
        return None
