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
    conn = sqlite3.connect("project_data.db")
    return conn

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

    for result in results:
        cursor.execute("""
        INSERT INTO processed_results 
        (chunk_text, positive_count, negative_count, sentiment_score, detected_keywords)
        VALUES (?, ?, ?, ?, ?)
        """, (
            result["chunk_text"],
            result["positive_count"],
            result["negative_count"],
            result["sentiment_score"],
            result["detected_keywords"]
        ))

    conn.commit()
    conn.close()