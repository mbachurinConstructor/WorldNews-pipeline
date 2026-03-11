from dotenv import load_dotenv
import os

load_dotenv()

news_api_key = os.getenv("NEWS_API_KEY")
news_api_url = "https://newsapi.org/v2/top-headlines"

aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_bucket_name = os.getenv("AWS_BUCKET_NAME")

postgres_host=os.getenv("POSTGRES_HOST")
postgres_port=os.getenv("POSTGRES_PORT")
postgres_db=os.getenv("POSTGRES_DB")
postgres_user=os.getenv("POSTGRES_USER")
postgres_password=os.getenv("POSTGRES_PASSWORD")

categories = ["technology", "business", "science", "health"]



if not news_api_key or not aws_access_key or not aws_secret_access_key or not aws_bucket_name or not news_api_url:
    raise ValueError("Some const not found in .env file")
