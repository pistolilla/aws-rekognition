# aws_rekognition
Sample web service for cloud image recognition using AWS Rekognition

This example is designed for [Serverless Framework](https://www.serverless.com/).

To deploy simply run:
```bash
# Serverless deployment credentials
export AWS_ACCESS_KEY_ID=<your_rekognition_key_here>
export AWS_SECRET_ACCESS_KEY=<your_rekognition_secret_key_here>

# Rekognition and S3 credentials
export BOTO_ACCESS_KEY_ID=<your_boto_access_key_id_here>
export BOTO_SECRET_ACCESS_KEY=<your_boto_secret_access_key_here>
export S3_BUCKET_NAME=<your_s3_bucket_name_here>
export S3_BUCKET_REGION=<your_s3_bucket_region_here>

sls deploy
```

To run tests, type
```bash
export TEST_URL=<url_provided_by_sls>
python3 runtests.py -v
```

Locally you can run tests like this
```bash
export TEST_URL=http://localhost:5000
python3 runtests.py -v
```