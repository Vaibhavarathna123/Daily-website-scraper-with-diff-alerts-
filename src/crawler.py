import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib
import time

visited = set()   # ✅ FIX ADDED

def get_hash(content):
    return hashlib.md5(content.encode("utf-8")).hexdigest()

def crawl(url, domain, max_pages=10):
    pages = {}
    stack = [url]

    while stack and len(pages) < max_pages:
        current = stack.pop()
        if current in visited:
            continue

        try:
            print(f"🔍 Crawling: {current}")

            r = requests.get(current, timeout=5)
            if r.status_code != 200:
                continue

            visited.add(current)
            soup = BeautifulSoup(r.text, "html.parser")
            pages[current] = get_hash(soup.get_text())

            for link in soup.find_all("a", href=True):
                next_url = urljoin(current, link["href"])
                if domain in urlparse(next_url).netloc:
                    stack.append(next_url)

            time.sleep(1)

        except Exception as e:
            print("❌ Error:", e)

    return pages
