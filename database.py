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

def setup_database():
    conn = sqlite3.connect("project_data.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sample_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        value INTEGER
    )
    """)

    data = [
        ("Sathvika", 60),
        ("Bhavana", 70),
        ("Saritha", 80),
        ("Maheswar", 90),
        ("Anvija", 100)
    ]

    cursor.executemany(
        "INSERT INTO sample_data (name, value) VALUES (?, ?)",
        data
    )

    conn.commit()
    conn.close()

    print("5 sample rows inserted successfully!")

if __name__ == "__main__":
    setup_database()