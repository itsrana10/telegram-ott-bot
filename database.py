import sqlite3

DB_NAME = "movies.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        file_id TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def add_movie(title, file_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO movies (title, file_id) VALUES (?, ?)",
        (title, file_id)
    )

    conn.commit()
    conn.close()

def get_movies():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT id, title, file_id FROM movies")
    movies = cur.fetchall()

    conn.close()
    return movies
