import requests
import sqlite3
import time
import string

conn = sqlite3.connect("all_books.db")
cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS books (
#     key TEXT PRIMARY KEY,
#     title TEXT,
#     author TEXT,
#     first_publish_year INTEGER
# )
# """)
# conn.commit()

# def fetch_books(query, page=1, limit=100):
#     url = f"https://openlibrary.org/search.json?q={query}&page={page}&limit={limit}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Failed for query={query} page={page}")
#         return None

# def save_books(docs):
#     for book in docs:
#         key = book.get("key")
#         title = book.get("title", "")
#         author = ", ".join(book.get("author_name", [])) if "author_name" in book else "Unknown"
#         year = book.get("first_publish_year", None)
#         try:
#             cursor.execute("""
#                 INSERT OR IGNORE INTO books (key, title, author, first_publish_year)
#                 VALUES (?, ?, ?, ?)
#             """, (key, title, author, year))
#         except Exception as e:
#             print("Error inserting:", e)
#     conn.commit()

# queries = list(string.ascii_lowercase) + list("0123456789")

# for q in queries:
#     print(f"Fetching books for query: '{q}'")
#     for page in range(1, 6):
#         print(f"  Page {page}")
#         data = fetch_books(q, page)
#         if data and "docs" in data:
#             save_books(data["docs"])
#         else:
#             break
#         time.sleep(1)

cursor.execute("""
SELECT first_publish_year, COUNT(*) as total_books
FROM books
WHERE first_publish_year IS NOT NULL
GROUP BY first_publish_year
ORDER BY first_publish_year
""")

results = cursor.fetchall()

print(f"{'ปี':<16} {'จำนวนหนังสือ':>15}")
print("-" * 30)
for year, count in results:
    print(f"{year:<8} {count:>15}")


cursor.execute("""
SELECT author, COUNT(*) as total_books
FROM books
WHERE author IS NOT NULL
GROUP BY author
ORDER BY total_books DESC
LIMIT 20  -- แสดงเฉพาะนักเขียนที่มีจำนวนหนังสือมากที่สุด 20 อันดับ
""")

author_results = cursor.fetchall()
conn.close()

print("\nจำนวนหนังสือต่อผู้แต่ง (Top 20)")
print(f"{'ผู้แต่ง':<50} {'จำนวนหนังสือ':>5}")
print("-" * 60)
for author, count in author_results:
    print(f"{author[:38]:<40} {count:>15}")