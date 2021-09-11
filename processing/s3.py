import os, boto3, uuid


S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
S3_BUCKET_REGION = os.environ['S3_BUCKET_REGION']

def presigned_post(filename=None, expiration=3600):
    if not filename:
        filename = str(uuid.uuid4())
    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3', region_name=S3_BUCKET_REGION)
    response = s3_client.generate_presigned_post(S3_BUCKET_NAME,
                filename,
                Fields=None,
                Conditions=None,
                ExpiresIn=expiration)
    return response

if __name__ == "__main__":
    #tests
    print(presigned_post("hoja"))