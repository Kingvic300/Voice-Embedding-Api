# db.py
import sqlite3

DB_PATH = "embeddings.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                embedding TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_embedding(embedding):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO embeddings (embedding) VALUES (?)",
            (embedding,)
        )
        file_id = cursor.lastrowid
        conn.commit()
    return file_id

def get_embedding_by_id(file_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT embedding, created_at FROM embeddings WHERE id = ?", (file_id,))
        return cursor.fetchone()
