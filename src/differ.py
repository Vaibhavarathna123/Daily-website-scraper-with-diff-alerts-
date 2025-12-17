from src.database import get_db

def detect_changes(new_pages):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT url, content_hash FROM pages")
    old_pages = dict(cur.fetchall())

    for url, hsh in new_pages.items():
        if url not in old_pages:
            cur.execute("INSERT INTO changes(url, change_type) VALUES (?,?)", (url, "NEW"))
        elif old_pages[url] != hsh:
            cur.execute("INSERT INTO changes(url, change_type) VALUES (?,?)", (url, "CHANGED"))

        cur.execute("REPLACE INTO pages(url, content_hash) VALUES (?,?)", (url, hsh))

    for url in old_pages:
        if url not in new_pages:
            cur.execute("INSERT INTO changes(url, change_type) VALUES (?,?)", (url, "REMOVED"))

    conn.commit()
    conn.close()
