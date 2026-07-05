import sqlite3
from pathlib import Path

from core.ranking import calculate_score

DB_PATH = Path("data/jarvis.db")


def search_files(query, limit=10):
    """
    Smart search for indexed files and folders.
    """

    query = query.lower().strip()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM files
    """)

    results = []

    for row in cursor.fetchall():

        item = dict(row)

        score = calculate_score(query, item)

        if score <= 0:
            continue

        results.append({
            "score": score,
            "data": item
        })

    conn.close()

    results.sort(
        key=lambda x: (
            x["score"],
            x["data"].get("modified", 0)
        ),
        reverse=True
    )

    return results[:limit]


if __name__ == "__main__":

    while True:

        q = input("\nSearch: ")

        if q.lower() == "exit":
            break

        matches = search_files(q)

        if not matches:
            print("Nothing found.")
            continue

        print()

        for i, item in enumerate(matches, 1):

            data = item["data"]

            print(
                f"{i}. "
                f"{data['name']} "
                f"({data.get('category', 'Unknown')}) "
                f"Score={item['score']:.2f}"
            )