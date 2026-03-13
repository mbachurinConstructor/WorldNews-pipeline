from aws.aws_s3_upload import upload_to_s3
from news_api.get_articles import get_articles
from consts.consts import categories


def get_data(categories: list[str]) -> list:
    data : list = []
    for category in categories:
        articles : list = get_articles(category)["articles"]
        for article in articles:
            data.append(article)
    print(f"Fetched {len(data)} articles")
    return data



def run_extract(categories: list[str] = categories) -> None:
    data : list = get_data(categories)
    upload_to_s3(data, "raw/")
