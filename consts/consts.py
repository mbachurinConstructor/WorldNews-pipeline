from dotenv import load_dotenv
import os

load_dotenv()

news_api_key : str = os.getenv("NEWS_API_KEY")
news_api_url : str = "https://newsapi.org/v2/top-headlines"

aws_access_key : str = os.getenv("AWS_ACCESS_KEY")
aws_secret_access_key : str = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_bucket_name : str = os.getenv("AWS_BUCKET_NAME")

postgres_host : str =os.getenv("POSTGRES_HOST")
postgres_port : str =os.getenv("POSTGRES_PORT")
postgres_db : str =os.getenv("POSTGRES_DB")
postgres_user : str =os.getenv("POSTGRES_USER")
postgres_password : str =os.getenv("POSTGRES_PASSWORD")

categories : list = [
    "technology",
    "business",
    "science",
    "health",
    "sports",
    "entertainment",
    "general"
]



if not news_api_key or not aws_access_key or not aws_secret_access_key or not aws_bucket_name or not news_api_url:
    raise ValueError("Some const not found in .env file")
