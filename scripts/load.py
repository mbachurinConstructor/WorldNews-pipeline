from scripts.db import init_db, load_articles
from aws.aws_download_from_s3 import download_from_s3

if __name__ == "__main__":
    data = download_from_s3("transformed/")

    init_db()
    load_articles(data)
    print(f"{len(data)} articles loaded")