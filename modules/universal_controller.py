import os

from modules.universal_search import search_apps
from modules.smart_search import search_files


def open_item(query):
    """
    Opens either an app or a file based on the best search result.
    """

    query = query.lower().strip()

    app_results = search_apps(query)
    file_results = search_files(query)

    candidates = []

    for item in app_results:
        candidates.append(item)

    for item in file_results:
        candidates.append({
            "type": "file",
            "score": item["score"],
            "data": item["data"]
        })

    if not candidates:
        print("Nothing found.")
        return False

    candidates.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    best = candidates[0]

    if best["type"] == "app":

        app = best["data"]

        try:

            if app["type"] == "desktop":
                os.startfile(app["path"])

            elif app["type"] == "uwp":
                os.system(f'explorer shell:AppsFolder\\{app["appid"]}')

            print(f"Opened {app['name']}")
            return True

        except Exception as e:
            print(e)
            return False

    elif best["type"] == "file":

        file = best["data"]

        try:

            os.startfile(file["path"])

            print(f"Opened {file['name']}")

            return True

        except Exception as e:
            print(e)
            return False


if __name__ == "__main__":

    while True:

        q = input("Open: ")

        if q.lower() == "exit":
            break

        open_item(q)