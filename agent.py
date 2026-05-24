"""
Daily Newspaper Agent — RSS Edition
─────────────────────────────────────
SETUP:
1. pip install requests schedule python-dotenv
2. Fill in your .env file
3. python agent.py --now    → test immediately
4. python agent.py          → runs daily at 7:00-7:30 AM
"""

import os, time, random, smtplib, logging, argparse, requests
import xml.etree.ElementTree as ET
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
from dotenv import load_dotenv

load_dotenv()
SENDER_EMAIL   = os.getenv("SENDER_EMAIL")
APP_PASSWORD   = os.getenv("APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# ── RSS Feeds ─────────────────────────────────────────────────────────────────
# Search-based URLs are stable and always return fresh real-time results
RSS_FEEDS = {
    "Top India News":    "https://news.google.com/rss/search?q=India+news+today&hl=en-IN&gl=IN&ceid=IN:en",
    "Business & Economy":"https://news.google.com/rss/search?q=India+business+economy+market&hl=en-IN&gl=IN&ceid=IN:en",
    "IPL & Cricket":     "https://news.google.com/rss/search?q=IPL+2026+cricket&hl=en-IN&gl=IN&ceid=IN:en",
    "Technology":        "https://news.google.com/rss/search?q=technology+AI+India&hl=en-IN&gl=IN&ceid=IN:en",
    "Sports":            "https://news.google.com/rss/search?q=India+sports+today&hl=en-IN&gl=IN&ceid=IN:en",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("agent.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

# ── Fetch RSS ─────────────────────────────────────────────────────────────────
SKIP_PHRASES = [
    "this feed is not available",
    "feed not available",
    "no results",
]

def fetch_rss(name: str, url: str, max_items: int = 8) -> list[dict]:
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        root = ET.fromstring(r.content)
        articles = []

        for item in root.findall(".//item"):
            title  = item.findtext("title", "").strip()
            link   = item.findtext("link",  "").strip()
            source = item.findtext("source", "").strip()

            # Skip placeholder / error messages from Google News
            if any(p in title.lower() for p in SKIP_PHRASES):
                continue

            # Clean title — Google News appends "- Source Name" at the end
            if " - " in title:
                title, source = title.rsplit(" - ", 1)

            articles.append({
                "title":  title.strip(),
                "link":   link,
                "source": source.strip(),
            })

            if len(articles) >= max_items:
                break

        log.info(f"[{name}] Fetched {len(articles)} articles.")
        return articles

    except Exception as e:
        log.error(f"[{name}] Failed: {e}")
        return []

def fetch_all_news() -> dict:
    all_news = {}
    for name, url in RSS_FEEDS.items():
        articles = fetch_rss(name, url)
        if articles:
            all_news[name] = articles
        time.sleep(1)
    return all_news

# ── Build HTML email ──────────────────────────────────────────────────────────
COLORS = {
    "Top India News":    "#1a73e8",
    "Business & Economy":"#0f9d58",
    "IPL & Cricket":     "#e8710a",
    "Technology":        "#9334e6",
    "Sports":            "#d93025",
}

def build_html(all_news: dict) -> str:
    today = datetime.now().strftime("%A, %d %B %Y")
    total = sum(len(v) for v in all_news.values())

    sections = ""
    for section, articles in all_news.items():
        color = COLORS.get(section, "#333")
        rows = ""
        for i, a in enumerate(articles, 1):
            rows += f"""
            <tr>
              <td style="padding:10px 0; border-bottom:1px solid #f0f0f0;">
                <span style="color:{color}; font-weight:700; font-size:12px;">#{i}</span>&nbsp;
                <a href="{a['link']}" style="color:#1a1a1a; text-decoration:none; font-size:14px; font-weight:500; line-height:1.5;">
                  {a['title']}
                </a><br>
                <span style="color:#999; font-size:12px;">{a['source']}</span>
              </td>
            </tr>"""

        sections += f"""
        <tr><td style="padding:24px 0 6px;">
          <table width="100%" cellpadding="0" cellspacing="0"><tr>
            <td style="border-left:4px solid {color}; padding-left:12px;">
              <h2 style="margin:0; font-size:15px; font-weight:700; color:{color};">{section}</h2>
            </td>
          </tr></table>
        </td></tr>
        <tr><td>
          <table width="100%" cellpadding="0" cellspacing="0">{rows}</table>
        </td></tr>"""

    if not sections:
        sections = "<tr><td style='padding:20px;text-align:center;color:#888;'>No news fetched. Check agent.log.</td></tr>"

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:24px 0;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">

  <tr><td style="background:linear-gradient(135deg,#1a73e8,#0d47a1);padding:32px 36px;">
    <h1 style="margin:0;color:#fff;font-size:22px;font-weight:700;">📰 Your Daily News Digest</h1>
    <p style="margin:6px 0 0;color:#c8dcff;font-size:14px;">{today}</p>
  </td></tr>

  <tr><td style="background:#f8f9ff;padding:12px 36px;border-bottom:1px solid #e8eaf0;">
    <p style="margin:0;font-size:13px;color:#555;">
      ✅ &nbsp;<strong>{total} fresh stories</strong> across <strong>{len(all_news)} categories</strong>
      &nbsp;—&nbsp; click any headline to read the full article.
    </p>
  </td></tr>

  <tr><td style="padding:8px 36px 24px;">
    <table width="100%" cellpadding="0" cellspacing="0">{sections}</table>
  </td></tr>

  <tr><td style="background:#f8f9ff;padding:16px 36px;border-top:1px solid #e8eaf0;text-align:center;">
    <p style="margin:0;font-size:12px;color:#aaa;">
      Delivered by your Daily Newspaper Agent &nbsp;·&nbsp; Powered by Google News RSS
    </p>
  </td></tr>

</table>
</td></tr></table>
</body></html>"""

# ── Send Email ────────────────────────────────────────────────────────────────
def send_email(all_news: dict) -> None:
    if not SENDER_EMAIL or not APP_PASSWORD:
        log.error("Credentials missing — check .env file.")
        return

    msg = MIMEMultipart("alternative")
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = RECEIVER_EMAIL
    msg["Subject"] = f"📰 Daily News Digest — {datetime.now().strftime('%d %b %Y')}"
    msg.attach(MIMEText(build_html(all_news), "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.ehlo(); s.starttls()
            s.login(SENDER_EMAIL, APP_PASSWORD)
            s.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        log.info("✓ Email sent successfully!")
    except Exception as e:
        log.error(f"Email failed: {e}")

# ── Main ──────────────────────────────────────────────────────────────────────
def run_job():
    log.info("=" * 55)
    log.info("Newspaper Agent — job started")
    log.info("=" * 55)
    all_news = fetch_all_news()
    send_email(all_news)
    log.info("Job complete.\n")

def scheduled_job():
    delay = random.randint(0, 30 * 60)
    log.info(f"Waiting {delay // 60} min before running…")
    time.sleep(delay)
    run_job()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--now", action="store_true")
    args = parser.parse_args()

    if args.now:
        run_job()
    else:
        log.info("Scheduler active — fires daily at 07:00 AM (+0-30 min jitter).")
        schedule.every().day.at("07:00").do(scheduled_job)
        while True:
            schedule.run_pending()
            time.sleep(30)