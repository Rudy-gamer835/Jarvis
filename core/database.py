import sqlite3
from pathlib import Path

DB_PATH = Path("data/jarvis.db")


def get_connection():
    """
    Returns SQLite connection.
    """

    DB_PATH.parent.mkdir(exist_ok=True)

    return sqlite3.connect(DB_PATH)


def initialize_database():
    """
    Creates the complete Jarvis database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # =====================================================
    # APPS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS apps(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        path TEXT,

        type TEXT,

        appid TEXT,

        keywords TEXT,

        priority INTEGER DEFAULT 1000
    )
    """)

    # =====================================================
    # FOLDERS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS folders(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        path TEXT UNIQUE NOT NULL,

        keywords TEXT,

        priority INTEGER DEFAULT 800
    )
    """)

    # =====================================================
    # FILES
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS files(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        path TEXT UNIQUE NOT NULL,

        extension TEXT,

        size INTEGER,

        modified REAL,

        drive TEXT,

        folder TEXT,

        parent_folder TEXT,

        category TEXT,

        keywords TEXT,

        is_folder INTEGER DEFAULT 0,

        priority INTEGER DEFAULT 200
    )
    """)

    # =====================================================
    # INDEXES
    # =====================================================

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_app_name
    ON apps(name)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_folder_name
    ON folders(name)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_file_name
    ON files(name)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_file_category
    ON files(category)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_parent_folder
    ON files(parent_folder)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_extension
    ON files(extension)
    """)

    conn.commit()
    conn.close()


def clear_database():
    """
    Clears every table.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("DELETE FROM apps")
    cursor.execute("DELETE FROM folders")
    cursor.execute("DELETE FROM files")

    conn.commit()
    conn.close()


if __name__ == "__main__":

    initialize_database()

    print("\n====================================")
    print("     JARVIS DATABASE READY")
    print("====================================")