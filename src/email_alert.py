import smtplib
from email.mime.text import MIMEText
from src.database import get_db

# ---------------- EMAIL CONFIG ----------------
EMAIL = "vaibhavav124@gmail.com"        # sender & receiver
APP_PASSWORD = "gqrh wbdi cdss ncdz"  # 16-char App Password

# ---------------- SEND EMAIL + STORE ALERT ----------------
def send_email():
    conn = get_db()
    cur = conn.cursor()

    # Fetch detected changes
    cur.execute("SELECT url, change_type FROM changes")
    rows = cur.fetchall()

    # If no changes, still store alert with zeros
    if not rows:
        message = (
            "NEW: 0 | CHANGED: 0 | REMOVED: 0 | "
            "Email sent to vaibhavav124@gmail.com"
        )

        cur.execute(
            "INSERT INTO alerts(message) VALUES (?)",
            (message,)
        )
        conn.commit()
        conn.close()
        return

    # ---------------- COUNT CHANGES ----------------
    new_count = sum(1 for _, c in rows if c == "NEW")
    changed_count = sum(1 for _, c in rows if c == "CHANGED")
    removed_count = sum(1 for _, c in rows if c == "REMOVED")

    # ---------------- EMAIL BODY ----------------
    body_lines = []
    for url, change_type in rows:
        body_lines.append(f"{change_type}: {url}")

    email_body = "\n".join(body_lines)

    msg = MIMEText(email_body)
    msg["Subject"] = "Daily Website Change Report"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    # ---------------- SEND EMAIL ----------------
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()

    # ---------------- STORE ALERT MESSAGE ----------------
    alert_message = (
        f"NEW: {new_count} | "
        f"CHANGED: {changed_count} | "
        f"REMOVED: {removed_count} | "
        f"Email sent to vaibhava124@gmail.com"
    )

    cur.execute(
        "INSERT INTO alerts(message) VALUES (?)",
        (alert_message,)
    )

    # ---------------- CLEAR CHANGES (IMPORTANT) ----------------
    cur.execute("DELETE FROM changes")

    conn.commit()
    conn.close()
