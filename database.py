# import sqlite3

# def setup_database():
#     conn = sqlite3.connect("project_data.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS sample_data (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         value INTEGER
#     )
#     """)

#     conn.commit()
#     conn.close()

#     print("Table created successfully!")

# if __name__ == "__main__":
#     setup_database()



import sqlite3

def create_connection():
    try:
        conn = sqlite3.connect("project_data.db")
        return conn
    except sqlite3.Error as e:
        print("Database connection error:", e)
        return None
def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processed_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chunk_text TEXT,
        positive_count INTEGER,
        negative_count INTEGER,
        sentiment_score INTEGER,
        detected_keywords TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_results(results):
    conn = create_connection()
    cursor = conn.cursor()

    data_to_insert = [
        (
            r["chunk_text"],
            r["positive_count"],
            r["negative_count"],
            r["sentiment_score"],
            r["detected_keywords"]
        )
        for r in results
    ]

    cursor.executemany("""
        INSERT INTO processed_results
        (chunk_text, positive_count, negative_count, sentiment_score, detected_keywords)
        VALUES (?, ?, ?, ?, ?)
    """, data_to_insert)

    conn.commit()
    conn.close()