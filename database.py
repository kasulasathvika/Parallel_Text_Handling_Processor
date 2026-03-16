import sqlite3
import time
import csv

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
def search_reviews(keyword=None, sentiment=None, min_score=None):
    conn = sqlite3.connect("project_data.db")
    cursor = conn.cursor()

    query = "SELECT review_text, score, sentiment, timestamp FROM processed_results WHERE 1=1"
    params = []

    if keyword:
        query += " AND review_text LIKE ?"
        params.append(f"%{keyword}%")

    if sentiment:
        query += " AND sentiment = ?"
        params.append(sentiment)

    if min_score is not None:
        query += " AND score >= ?"
        params.append(min_score)

    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()
    return results

def export_to_csv(filename="exported_results.csv"):
    conn = sqlite3.connect("project_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT review_text, score, sentiment, timestamp FROM processed_results")
    rows = cursor.fetchall()

    conn.close()

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["review_text", "score", "sentiment", "timestamp"])
        writer.writerows(rows)

    print("Results exported to", filename)