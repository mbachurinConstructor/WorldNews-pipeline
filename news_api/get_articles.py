import requests
from datetime import datetime

from consts.consts import news_api_key, news_api_url

def get_articles(category: str) -> dict or list:
    response : requests.Response = requests.get(news_api_url, params={
        "apiKey": news_api_key,
        "category": category,
        "language": "en",
        "pageSize":100,
    }
                            )
    now : str = datetime.now().isoformat()
    data : dict = response.json()

    if data["status"] != "ok":
        raise Exception("Failed to Fetch Articles")
    else:
        for each in data["articles"]:
            each["fetchedAt"] = now
            each["category"] = category
        return data