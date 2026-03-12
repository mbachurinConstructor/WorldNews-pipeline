from scripts.db import get_connection

queries = {
    "Top 10 sources": """
        SELECT source_name, COUNT(*) as source_count
        FROM articles
        GROUP BY source_name
        ORDER BY source_count DESC
        LIMIT 10
    """,
    "Articles per category": """
        SELECT category, COUNT(*) as category_count
        FROM articles
        GROUP BY category
        ORDER BY category_count DESC
    """,
    "Top 10 authors": """
        SELECT author, COUNT(*) as author_count
        FROM articles
        WHERE author != 'unknown'
        GROUP BY author
        ORDER BY author_count DESC
        LIMIT 10
    """,
    "Latest 5 articles": """
        SELECT title, source_name, published_at
        FROM articles
        ORDER BY published_at DESC
        LIMIT 5
    """,
}

def display_row(row):
    key, count = row[0], row[1]
    print(f"{key} - {count}")


def run_analytics():
    connection = get_connection()
    cursor = connection.cursor()
    for name, query in queries.items():
        print(f"{name}")
        cursor.execute(query)
        for row in cursor.fetchall():
            display_row(row)
        print("\n\n\n")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    run_analytics()