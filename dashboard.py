import streamlit as st
import sqlite3
import pandas as pd
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Website Diff Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- DARK THEME CSS ----------------
st.markdown("""
<style>
.stApp { background-color: #0e1117; color: white; }
h1, h2, h3 { color: #f1f1f1; }
.metric-card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 0 12px rgba(0,255,255,0.2);
}
.metric-title { font-size: 18px; color: #9ca3af; }
.metric-value { font-size: 36px; font-weight: bold; }
hr { border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1>🌐 Daily Website Diff Scraper Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#9ca3af'>Monitor crawled pages and website changes</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- DB CONNECTION ----------------
conn = sqlite3.connect("data/scraper.db")

pages_df = pd.read_sql("SELECT * FROM pages", conn)
changes_df = pd.read_sql("SELECT * FROM changes", conn)

# ---------------- READ LATEST ALERT ----------------
try:
    alert_df = pd.read_sql(
        "SELECT message, timestamp FROM alerts ORDER BY timestamp DESC LIMIT 1",
        conn
    )
except:
    alert_df = pd.DataFrame()

# ---------------- CHANGE SUMMARY LOGIC ----------------
new_count = changed_count = removed_count = 0

if not alert_df.empty:
    msg = alert_df.iloc[0]["message"]

    # Example expected message:
    # "NEW: 2 | CHANGED: 1 | REMOVED: 0 | Email sent to vaibhava124@gmail.com"

    new_match = re.search(r"NEW:\s*(\d+)", msg)
    changed_match = re.search(r"CHANGED:\s*(\d+)", msg)
    removed_match = re.search(r"REMOVED:\s*(\d+)", msg)

    if new_match:
        new_count = int(new_match.group(1))
    if changed_match:
        changed_count = int(changed_match.group(1))
    if removed_match:
        removed_count = int(removed_match.group(1))

# ---------------- EMAIL STATUS ----------------
if not alert_df.empty:
    st.success(f"📧 {alert_df.iloc[0]['message']} ⏰ {alert_df.iloc[0]['timestamp']}")
else:
    st.info("📧 No email alerts sent yet.")

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- METRICS ----------------
st.subheader("📊 Change Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🆕 NEW</div>
        <div class="metric-value" style="color:#22c55e;">{new_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">✏️ CHANGED</div>
        <div class="metric-value" style="color:#facc15;">{changed_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">❌ REMOVED</div>
        <div class="metric-value" style="color:#ef4444;">{removed_count}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- CRAWLED PAGES ----------------
st.subheader("🌍 Crawled Pages")
st.dataframe(pages_df, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- CHANGE HISTORY ----------------
st.subheader("🔄 Change History")

if changes_df.empty:
    st.info("No active changes. Latest changes were already notified via email.")
else:
    st.dataframe(changes_df, use_container_width=True)

conn.close()

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("🖤 Built with Python • SQLite • Streamlit (Dark Theme)")
