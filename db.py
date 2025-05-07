import requests
import sqlite3
import time
import string

# สร้างฐานข้อมูล
conn = sqlite3.connect("all_books.db")
cursor = conn.cursor()

# สร้างตาราง
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    key TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    first_publish_year INTEGER
)
""")
conn.commit()

def fetch_books(query, page=1, limit=100):
    url = f"https://openlibrary.org/search.json?q={query}&page={page}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed for query={query} page={page}")
        return None

def save_books(docs):
    for book in docs:
        key = book.get("key")
        title = book.get("title", "")
        author = ", ".join(book.get("author_name", [])) if "author_name" in book else "Unknown"
        year = book.get("first_publish_year", None)
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO books (key, title, author, first_publish_year)
                VALUES (?, ?, ?, ?)
            """, (key, title, author, year))
        except Exception as e:
            print("Error inserting:", e)
    conn.commit()

# ใช้ a-z, 0-9 เป็นคำค้นเริ่มต้น
queries = list(string.ascii_lowercase) + list("0123456789")

for q in queries:
    print(f"Fetching books for query: '{q}'")
    for page in range(1, 6):  # ดึงหน้า 1 ถึง 5 ต่อ query (เปลี่ยนจำนวนได้)
        print(f"  Page {page}")
        data = fetch_books(q, page)
        if data and "docs" in data:
            save_books(data["docs"])
        else:
            break
        time.sleep(1)  # ชะลอการเรียก API เพื่อไม่ให้โดนบล็อก

# ดึงข้อมูล: จำนวนหนังสือต่อปี
cursor.execute("""
SELECT first_publish_year, COUNT(*) as total_books
FROM books
WHERE first_publish_year IS NOT NULL
GROUP BY first_publish_year
ORDER BY first_publish_year
""")

results = cursor.fetchall()
conn.close()

# แสดงผลลัพธ์ใน terminal
print(f"{'ปี':<8} {'จำนวนหนังสือ':>15}")
print("-" * 25)
for year, count in results:
    print(f"{year:<8} {count:>15}")


conn.close()