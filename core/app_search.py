import sqlite3
from difflib import SequenceMatcher
from pathlib import Path
import json

APP_DB = Path("data/apps.json")
FILE_DB = Path("data/jarvis.db")


def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def search_apps(query):
    """
    Search installed applications.
    """

    if not APP_DB.exists():
        return []

    with open(APP_DB, "r", encoding="utf-8") as f:
        apps = json.load(f)

    results = []

    query = query.lower()

    for key, app in apps.items():

        score = 0

        name = app["name"].lower()

        if query == name:
            score += 100

        if query in name:
            score += 80

        score += similarity(query, name) * 50

        for alias in app.get("aliases", []):

            alias = alias.lower()

            if query == alias:
                score += 90

            elif query in alias:
                score += 70

        if score > 40:

            results.append({
                "type": "app",
                "score": score,
                "data": app
            })

    return results


def search_files(query):
    """
    Search indexed files.
    """

    if not FILE_DB.exists():
        return []

    conn = sqlite3.connect(FILE_DB)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM files
        WHERE LOWER(name) LIKE ?
        LIMIT 100
    """, (f"%{query.lower()}%",))

    rows = cursor.fetchall()

    conn.close()

    results = []

    for row in rows:

        score = 0

        name = row["name"].lower()

        if query == name:
            score += 100

        if query in name:
            score += 80

        score += similarity(query, name) * 50

        results.append({

            "type": "file",

            "score": score,

            "data": dict(row)
        })

    return results


def universal_search(query):

    results = []

    results.extend(search_apps(query))
    results.extend(search_files(query))

    if not results:
        return None

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results


if __name__ == "__main__":

    while True:

        q = input("\nSearch: ")

        if q.lower() == "exit":
            break

        matches = universal_search(q)

        if not matches:
            print("Nothing found.")
            continue

        print()

        for i, item in enumerate(matches[:10], 1):

            print(
                f"{i}. "
                f"{item['type'].upper()} | "
                f"{item['score']:.1f} | "
                f"{item['data']['name']}"
            )