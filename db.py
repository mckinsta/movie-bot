import sqlite3

conn = sqlite3.connect("movies.db", check_same_thread=False)
cur = conn.cursor()

# 🧱 Table create (with part support)
cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    part INTEGER DEFAULT 1,
    file_id TEXT
)
""")

# ⚡ Index for fast search
cur.execute("CREATE INDEX IF NOT EXISTS idx_name ON movies(name)")
conn.commit()


# 📥 Save movie (auto detect part from name like def add_movie(name, file_id):
def add_movie(name, file_id):   # ✅ function start

    name = name.lower().strip()

    # remove .mp4
    if name.endswith(".mp4"):
        name = name.replace(".mp4", "")

    # split part
    if "_" in name:
        movie_name, part = name.split("_")
    else:
        movie_name = name
        part = int(part)

    cur.execute(
        "INSERT INTO movies (name, part, file_id) VALUES (?, ?, ?)",
        (movie_name, part, file_id)
    )
    conn.commit()


# 🔍 Get all parts of a movie
def get_parts(name):
    name = name.lower().strip()   # ✅ ADD THIS
    cur.execute(
        "SELECT part FROM movies WHERE name=? ORDER BY part",
        (name,)
    )
    return [row[0] for row in cur.fetchall()]


# 🎬 Get specific part file_id
def get_movie_by_part(name, part):
    name = name.lower().strip()   # ✅ ADD THIS
    cur.execute(
        "SELECT file_id FROM movies WHERE name=? AND part=?",
        (name, part)
    )
    result = cur.fetchone()
    return result[0] if result else None


# 🔎 (Optional) Old search (if needed)
def search_movie(query):
    query = f"%{query.lower()}%"

    cur.execute("""
    SELECT name, file_id 
    FROM movies 
    WHERE name LIKE ?
    LIMIT 1
    """, (query,))

    return cur.fetchone()
