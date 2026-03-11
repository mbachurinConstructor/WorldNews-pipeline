from aws.aws_s3_upload import upload_to_s3
from aws.aws_download_from_s3 import download_from_s3


def flatten_article(article: dict) -> dict:
    article["source_id"] = article["source"]["id"]
    article["source_name"] = article["source"]["name"]
    del article["source"]
    return article

def handle_nulls(article: dict) -> dict:
    for key in article:
        if article[key] is None:
            article[key] = "unknown"
    return article

def normalize_timestamp(article: dict, tag: str = "publishedAt") -> dict:
    article[tag] = article[tag].replace("T", " ")
    article[tag] = article[tag].replace("Z", "")
    return article

def remove_fields(article: dict) -> dict:
    del article["content"]
    del article["urlToImage"]
    return article

def transform_data(data:list) -> list:
    for i, article in enumerate(data):
        data[i] = remove_fields(data[i])
        data[i] = flatten_article(data[i])
        data[i] = normalize_timestamp(data[i], tag="publishedAt")
        data[i] = normalize_timestamp(data[i], tag="fetchedAt")
        data[i] = handle_nulls(data[i])
    return data

def run_transform(folder: str = "raw/"):
    raw_data = download_from_s3(folder)
    transformed_data = transform_data(raw_data)
    upload_to_s3(transformed_data, key="transformed/")
    print(f"Transformed {len(transformed_data)} articles")