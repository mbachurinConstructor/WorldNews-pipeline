import json
from boto3 import Session

from aws.aws_s3_client import get_s3_client
from consts.consts import aws_bucket_name

s3 : Session = get_s3_client()

def get_latest_bucket_object(folder: str) -> str:
    response = s3.list_objects_v2(Bucket=aws_bucket_name, Prefix=folder)
    latest : dict = sorted(response["Contents"], key=lambda k: k["LastModified"])[-1]
    return latest["Key"]

def download_from_s3(folder: str, key: str = None) -> list:
    if not key:
        key : str = get_latest_bucket_object(folder)
    response = s3.get_object(Bucket=aws_bucket_name, Key=key)
    data : list = json.loads(response["Body"].read().decode("utf-8"))
    return data