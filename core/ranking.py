from difflib import SequenceMatcher


def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def calculate_score(query, item):

    query = query.lower().strip()

    words = query.split()

    name = item.get("name", "").lower()
    folder = item.get("folder", "").lower()
    parent = item.get("parent_folder", "").lower()
    category = item.get("category", "").lower()
    keywords = item.get("keywords", "").lower()

    score = 0

    for word in words:

        # Exact filename
        if word == name:
            score += 500

        # Starts with
        if name.startswith(word):
            score += 300

        # Contains
        if word in name:
            score += 180

        if word in folder:
            score += 80

        if word in parent:
            score += 120

        if word in category:
            score += 100

        if word in keywords:
            score += 120

    score += similarity(query, name) * 100

    return score