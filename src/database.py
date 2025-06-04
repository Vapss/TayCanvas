import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "canvas_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS canvas_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_id TEXT,
            song_name TEXT,
            album_name TEXT,
            canvas_url TEXT,
            retrieved_at TEXT,
            UNIQUE(track_id, canvas_url) ON CONFLICT IGNORE
        )
        """
    )
    conn.commit()
    conn.close()


def insert_canvas(track_id: str, song_name: str, album_name: str, canvas_url: str, retrieved_at: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO canvas_history (track_id, song_name, album_name, canvas_url, retrieved_at) VALUES (?, ?, ?, ?, ?)",
        (track_id, song_name, album_name, canvas_url, retrieved_at),
    )
    conn.commit()
    conn.close()
