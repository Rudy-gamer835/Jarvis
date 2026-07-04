import sqlite3
from pathlib import Path
from difflib import get_close_matches

DB_PATH = Path("data/jarvis.db")


def search_file(query):
    """
    Search a file by exact, partial or fuzzy name.
    Returns the best matching file or None.
    """

    query = query.lower().strip()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Exact match
    cursor.execute(
        "SELECT * FROM files WHERE LOWER(name)=?",
        (query,)
    )

    result = cursor.fetchone()

    if result:
        conn.close()
        return dict(result)

    # 2. Partial match
    cursor.execute(
        "SELECT * FROM files WHERE LOWER(name) LIKE ? LIMIT 20",
        (f"%{query}%",)
    )

    rows = cursor.fetchall()

    if rows:

        if len(rows) == 1:
            conn.close()
            return dict(rows[0])

        names = [row["name"] for row in rows]

        match = get_close_matches(query, names, n=1, cutoff=0.4)

        if match:
            for row in rows:
                if row["name"] == match[0]:
                    conn.close()
                    return dict(row)

        conn.close()
        return dict(rows[0])

    conn.close()
    return None


if __name__ == "__main__":

    while True:

        query = input("Search File: ")

        if query.lower() == "exit":
            break

        result = search_file(query)

        print(result)