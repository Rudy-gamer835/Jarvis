import sqlite3

conn = sqlite3.connect("data/jarvis.db")

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM files")

print(cursor.fetchone())

conn.close()