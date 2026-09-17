import sqlite3

def init_db():
    conn = sqlite3.connect("data/journal.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id TEXT PRIMARY KEY,
            text TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            emotion TEXT,
            intensity INTEGER,
            themes TEXT,
            summary TEXT
        )
    """)
    conn.commit()
    return conn