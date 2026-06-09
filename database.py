import sqlite3

DB = "movies.db"

def init():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id TEXT PRIMARY KEY,
        title TEXT,
        file_id TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_movie(movie_id, title, file_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO movies VALUES (?, ?, ?)",
              (movie_id, title, file_id))
    conn.commit()
    conn.close()

def get_movies():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, title, file_id FROM movies")
    rows = c.fetchall()
    conn.close()

    return [
        {"id": r[0], "title": r[1], "file_id": r[2]}
        for r in rows
    ]

def get_movie(movie_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, title, file_id FROM movies WHERE id=?", (movie_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return {"id": row[0], "title": row[1], "file_id": row[2]}
    return None
