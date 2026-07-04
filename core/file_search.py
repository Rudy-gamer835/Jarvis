import sqlite3
from pathlib import Path

DB_PATH = Path("data/jarvis.db")


def search_files(query, limit=10):
    """
    Smart search for indexed files.
    """

    query = query.lower().strip()
    words = query.split()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM files
    """)

    results = []

    for row in cursor.fetchall():

        score = 0

        name = row["name"].lower()
        folder = (row["folder"] or "").lower()
        parent = (row["parent_folder"] or "").lower()
        category = (row["category"] or "").lower()
        keywords = (row["keywords"] or "").lower()

        for word in words:

            if word in name:
                score += 100

            if word in folder:
                score += 40

            if word in parent:
                score += 60

            if word in category:
                score += 70

            if word in keywords:
                score += 80

        if score > 0:
            results.append({
                "score": score,
                "data": dict(row)
            })

    conn.close()

    results.sort(
        key=lambda x: (x["score"], x["data"]["modified"]),
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
                f"({data['category']}) "
                f"Score={item['score']}"
            )