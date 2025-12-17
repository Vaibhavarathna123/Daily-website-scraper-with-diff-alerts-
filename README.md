# 🌐 Daily website scraper with “diff” alerts 

## 🚀 Project Overview
The **Daily Website Diff Scraper** is an automated website monitoring tool designed
to crawl a target domain daily, track changes in content, and notify the user via
**email alerts** and a **real-time dashboard**.

The scraper stores snapshots of web page content hashes and uses a differential
algorithm to categorize changes as:

- **NEW** – Newly discovered pages
- **CHANGED** – Existing pages with updated content
- **REMOVED** – Pages that no longer exist

The system consists of a polite web crawler, a SQLite database for persistence,
a diff engine, an email alert module, and a Streamlit-based dashboard.

---

## ✨ Features
- **Full-Domain Crawl**  
  Recursively crawls all pages within the specified domain.

- **Change Detection**  
  Uses **MD5 hashing** to detect content changes between crawls.

- **Email Alerts**  
  Sends a daily summary email showing counts of new, changed, and removed pages.

- **Interactive Dashboard**  
  A **Streamlit dashboard** to visualize crawl results, change history, and alerts.

- **Polite Crawling**  
  Includes a **1-second delay** between requests to respect server load.

---

## 🛠️ Libraries Used
The project uses the following Python libraries:

- **requests** – Fetch web pages  
- **beautifulsoup4** – Parse HTML and extract text  
- **sqlite3** – Persistent storage  
- **schedule** – Daily task scheduling  
- **smtplib**, **email.mime** – Email notifications  
- **pandas** – Data handling for dashboard  
- **streamlit** – Interactive web dashboard  

---

## 📂 Project Structure
```text
daily-website-diff-scraper
│
├── src
│   ├── crawler.py
│   ├── database.py
│   ├── differ.py
│   ├── email_alert.py
│   └── scheduler.py
│
├── data
│   └── scraper.db
│
├── tests
│   └── test_diff.py
│
├── main.py
├── requirements.txt
└── README.md
```


---

## ⚙️ Environment Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/daily-website-diff-scraper.git
cd daily-website-diff-scraper
```

### 2️⃣ Create a Virtual Environment (Recommended)
Run the following command to create the environment:

```Bash
python -m venv .venv
```

### Activate the virtual environment:
#### Linux / macOS:

``` Bash
source .venv/bin/activate
```
#### Windows:
``` Bash
.venv\Scripts\activate
```

### 3️⃣ Install Dependencies
Install the required packages using pip:
``` Bash
pip install -r requirements.txt
```

### ✉️ Email Configuration
Open src/email_alert.py and update the following variables:
```Python
EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_16_char_app_password"
```

### ▶️ How to Run the Project
- A️. Run Once (Testing)
To run the scraper a single time for testing purposes:
```Bash
python main.py
```
- B️. Run as a Daily Scheduler
To keep the script running on a schedule:
```Bash
python src/scheduler.py
```
Note: If main.py already calls run_once(), use main.py as the primary entry point.

### 📊 Run the Dashboard
To launch the visual dashboard:
``` Bash
streamlit run dashboard.py
```
The dashboard shows:
- Change Summary
- Email alerts
- Crawled Pages
- Change history

## 🗄️ Database Schema (data/scraper.db)

### 📄 pages
Stores the latest snapshot of crawled URLs.

| Column | Description |
| :--- | :--- |
| **url** | Page URL (Primary Key) |
| **content_hash** | MD5 content hash |

### 🔄 changes
Temporary table holding detected changes.

| Column | Description |
| :--- | :--- |
| **url** | Page URL |
| **change_type** | NEW / CHANGED / REMOVED |

### 📧 alerts
Stores crawl and email history.

| Column | Description |
| :--- | :--- |
| **message** | Summary message |
| **timestamp** | Event time |

**Example message:**
> NEW: 0 | CHANGED: 8 | REMOVED: 0 | Email sent successfully

---

## 🧪 Unit Testing

- **Unit tests implemented using pytest**
- **Core diff logic verified using automated test cases**
- Tests ensure correct detection of **NEW**, **CHANGED**, and **REMOVED** pages
- Test files are located in the `tests/` directory

Run tests using:
```bash
pytest
```
