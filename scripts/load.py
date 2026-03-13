from scripts.db import init_db, load_articles
from aws.aws_download_from_s3 import download_from_s3

def load_to_db() -> None:
    data : list = download_from_s3("transformed/")
    init_db()
    load_articles(data)
