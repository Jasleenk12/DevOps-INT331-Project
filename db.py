# db.py
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path("app.db")

@contextmanager
def conn_cursor():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        yield con, cur
        con.commit()
    finally:
        con.close()

def init_db():
    with conn_cursor() as (con, cur):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            mood TEXT NOT NULL,
            url TEXT
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS mood_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text_input TEXT,
            detected_mood TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """)

def add_user(username, password_hash):
    with conn_cursor() as (con, cur):
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?,?)", (username, password_hash))

def get_user(username):
    with conn_cursor() as (con, cur):
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        return cur.fetchone()

def insert_mood(user_id, text_input, detected_mood):
    with conn_cursor() as (con, cur):
        cur.execute("INSERT INTO mood_history (user_id, text_input, detected_mood) VALUES (?,?,?)",
                    (user_id, text_input, detected_mood))

def get_mood_history(user_id, limit=1000):
    with conn_cursor() as (con, cur):
        cur.execute("""
            SELECT detected_mood, created_at FROM mood_history
            WHERE user_id=? ORDER BY created_at DESC LIMIT ?
        """, (user_id, limit))
        return cur.fetchall()

def add_song(title, artist, mood, url=None):
    with conn_cursor() as (con, cur):
        cur.execute("INSERT INTO songs (title, artist, mood, url) VALUES (?,?,?,?)",
                    (title, artist, mood.lower(), url))

def delete_all_songs():
    with conn_cursor() as (con, cur):
        cur.execute("DELETE FROM songs")

def fetch_songs_by_mood(mood, limit=30):
    with conn_cursor() as (con, cur):
        cur.execute("""
            SELECT title, artist, mood, IFNULL(url,'') as url
            FROM songs WHERE LOWER(mood)=LOWER(?) LIMIT ?
        """, (mood, limit))
        return cur.fetchall()

def bulk_add_songs(rows):  # rows: list of (title, artist, mood, url)
    with conn_cursor() as (con, cur):
        cur.executemany("INSERT INTO songs (title, artist, mood, url) VALUES (?,?,?,?)", rows)

