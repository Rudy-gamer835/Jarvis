import json
from pathlib import Path
from difflib import get_close_matches

DB_FILE = Path("data/apps.json")


def load_apps():
    """Load the application database."""

    if not DB_FILE.exists():
        return {}

    with open(DB_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def find_app(query: str):
    """
    Find an application using:
    1. Exact match
    2. Alias match
    3. Partial match
    4. Fuzzy match
    """

    apps = load_apps()

    query = query.lower().strip()

    # ---------------- Exact Match ----------------
    if query in apps:
        return apps[query]

    # ---------------- Alias Match ----------------
    for app in apps.values():

        aliases = app.get("aliases", [])

        if query in [alias.lower() for alias in aliases]:
            return app

    # ---------------- Partial Match ----------------
    for name, app in apps.items():

        if query in name:
            return app

    # ---------------- Fuzzy Match ----------------
    matches = get_close_matches(
        query,
        apps.keys(),
        n=1,
        cutoff=0.6
    )

    if matches:
        return apps[matches[0]]

    return None


if __name__ == "__main__":

    while True:

        query = input("Search App: ")

        if query.lower() == "exit":
            break

        result = find_app(query)

        print(result)