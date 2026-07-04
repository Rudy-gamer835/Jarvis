import sqlite3
from pathlib import Path

DB_PATH = Path("data/jarvis.db")


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- APPS ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS apps(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        path TEXT,

        type TEXT,

        appid TEXT,

        keywords TEXT,

        priority INTEGER DEFAULT 1000
    )
    """)

    # ---------------- FOLDERS ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS folders(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        path TEXT UNIQUE,

        keywords TEXT,

        priority INTEGER DEFAULT 800
    )
    """)

    # ---------------- FILES ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS files(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        path TEXT UNIQUE,

        extension TEXT,

        category TEXT,

        keywords TEXT,

        modified REAL,

        priority INTEGER DEFAULT 200
    )
    """)

    # ---------- INDEXES ----------

    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_app_name ON apps(name)"
    )

    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_folder_name ON folders(name)"
    )

    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_file_name ON files(name)"
    )

    conn.commit()
    conn.close()


def clear_database():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("DELETE FROM apps")
    cur.execute("DELETE FROM folders")
    cur.execute("DELETE FROM files")

    conn.commit()
    conn.close()


if __name__ == "__main__":

    initialize_database()

    print("\nJarvis Database Ready.")