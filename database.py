import sqlite3
import time

DB_NAME="project_data.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processed_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        review_text TEXT,
        score INTEGER,
        sentiment TEXT,
        timestamp TEXT
    )
    """)
    cursor.execute("DELETE from processed_results")

    conn.commit()
    conn.close()


def insert_results(results):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.executemany("""
    INSERT INTO processed_results (review_text, score, sentiment,timestamp)
    VALUES (?, ?, ?, ?)
    """, [
        (r["review_text"], r["score"], r["sentiment"],r["timestamp"])
        for chunk in results
        for r in chunk
    ])

    conn.commit()
    conn.close()


def create_index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_sentiment
    ON processed_results(sentiment)
    """)

    conn.commit()
    conn.close()

def drop_index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DROP INDEX IF EXISTS idx_sentiment")

    conn.commit()
    conn.close()

def measure_query_time():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    start = time.time()
    cursor.execute("SELECT * FROM processed_results WHERE sentiment = 'Positive'")
    cursor.fetchall()
    end = time.time()

    print("Query Time:", round(end - start, 4), "seconds")

    conn.close()