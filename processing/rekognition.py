
import os, boto3

BOTO_ACCESS_KEY_ID = os.environ['BOTO_ACCESS_KEY_ID']
BOTO_SECRET_ACCESS_KEY = os.environ['BOTO_SECRET_ACCESS_KEY']
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
S3_BUCKET_REGION = os.environ['S3_BUCKET_REGION']

def detect_labels(photo):
    client=boto3.client('rekognition',
        region_name=S3_BUCKET_REGION,
        aws_access_key_id=BOTO_ACCESS_KEY_ID,
        aws_secret_access_key=BOTO_SECRET_ACCESS_KEY)
    Image = {
        'S3Object': {
            'Bucket': S3_BUCKET_NAME,
            'Name': photo
            }
        }
    response = client.detect_labels(Image=Image)
    return response['Labels']

if __name__ == "__main__":
    #tests
    print(detect_labels('test1.jpeg'))