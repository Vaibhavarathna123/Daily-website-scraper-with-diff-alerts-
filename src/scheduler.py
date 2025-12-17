import schedule
import time
from src.crawler import crawl
from src.differ import detect_changes
from src.email_alert import send_email
from src.database import init_db

def job():
    domain = "timeanddate.com"
    start_url = "https://www.timeanddate.com/weather/india/bengaluru"

    pages = crawl(start_url, domain)
    detect_changes(pages)
    send_email()

def start():
    init_db()
    print("✅ Scheduler started...")
    print("⏳ Waiting for scheduled crawl...")

    schedule.every().day.at("09:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)

# 🔥 ADD THIS FUNCTION (IMPORTANT)
def run_once():
    init_db()
    print("🚀 Running crawl once...")
    job()
    print("✅ Crawl finished")
