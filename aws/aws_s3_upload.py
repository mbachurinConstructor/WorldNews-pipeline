from datetime import datetime
import json

from aws.aws_s3_client import get_s3_client
from consts.consts import aws_bucket_name

s3 = get_s3_client()

def upload_to_s3(data: list, key : str = None) -> None:
    if key is None:
        key = f"raw/{datetime.now().isoformat()}.json"
    else:
        key += f"{datetime.now().isoformat()}.json"
    body = json.dumps(data, indent=2)
    s3.put_object(
        Bucket=aws_bucket_name,
        Key=key,
        Body=body,
        ContentType="application/json"
    )
    print(f"Uploaded to S3: {key}")