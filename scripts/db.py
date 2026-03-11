import psycopg2
from consts.consts import postgres_host, postgres_port, postgres_db, postgres_user, postgres_password

def get_connection():
    return psycopg2.connect(
        host=postgres_host,
        port=postgres_port,
        dbname=postgres_db,
        user=postgres_user,
        password=postgres_password,
    )

def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles(
            id SERIAL PRIMARY KEY, 
            author TEXT, 
            title TEXT,
            description TEXT,
            url TEXT UNIQUE NOT NULL,
            category TEXT, 
            source_id TEXT,
            source_name TEXT,
            published_at TIMESTAMP, 
            fetched_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized")

def insert_article(cursor, article: dict) -> None:
    cursor.execute("""
        INSERT INTO articles(
                author, 
                title, 
                description, 
                url, 
                category, 
                source_id, 
                source_name, 
                published_at, 
                fetched_at
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING
    """,
                   (
                       article["author"],
                       article["title"],
                       article["description"],
                       article["url"],
                       article["category"],
                       article["source_id"],
                       article["source_name"],
                       article["publishedAt"],
                       article["fetchedAt"],
                   )
                   )

def load_articles(articles: list) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    for article in articles:
        insert_article(cursor, article)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"{len(articles)} articles loaded")