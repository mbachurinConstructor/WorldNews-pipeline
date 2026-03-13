import boto3

from consts.consts import aws_access_key, aws_secret_access_key

def get_s3_client() -> boto3.Session:
    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
        region_name="us-east-1",
    )