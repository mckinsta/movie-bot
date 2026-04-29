import sqlite3

conn = sqlite3.connect("movies.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    file_id TEXT
)
""")

cur.execute("CREATE INDEX IF NOT EXISTS idx_name ON movies(name)")
conn.commit()

def add_movie(name, file_id):
    name = name.lower().strip()
    cur.execute("INSERT INTO movies (name, file_id) VALUES (?, ?)", (name, file_id))
    conn.commit()

def search_movie(query):
    query = f"%{query.lower()}%"

    cur.execute("""
    SELECT name, file_id 
    FROM movies 
    WHERE name LIKE ?
    LIMIT 1
    """, (query,))

    return cur.fetchone()
from db import add_movie, search_movie
