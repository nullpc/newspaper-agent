# 📰 Daily Newspaper Agent

An automated Python agent that delivers a **daily news digest to your email every morning at 7:00 AM IST** — completely hands-free, even when your PC is off.

Built with Python and powered by GitHub Actions for free cloud scheduling.

---

## 📧 Sample Output

Every morning you receive a clean formatted email like this:

- ✅ 25+ fresh stories across 5 categories
- 🇮🇳 Top India News
- 💼 Business & Economy
- 🏏 IPL & Cricket
- 💻 Technology
- 🏅 Sports

Each headline is clickable and links directly to the full article.

---

## ⚙️ How It Works

```
GitHub Actions (cron: 7:00 AM IST)
        ↓
Fetches Google News RSS Feeds
        ↓
Builds formatted HTML email
        ↓
Sends to your Gmail inbox
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core scripting language |
| requests | Fetching RSS feeds |
| BeautifulSoup4 | Parsing XML/HTML |
| smtplib | Sending emails via Gmail |
| python-dotenv | Managing credentials locally |
| GitHub Actions | Free cloud scheduling (cron job) |
| GitHub Secrets | Secure credential storage |

---

## 📁 Project Structure

```
newspaper-agent/
├── .github/
│   └── workflows/
│       └── newspaper.yml   # GitHub Actions workflow
├── agent.py                # Main Python script
├── .gitignore              # Keeps .env and venv out of repo
└── README.md               # You are here
```

---

## 🚀 Setup & Usage

### 1. Clone the repo
```bash
git clone https://github.com/nullpc/newspaper-agent.git
cd newspaper-agent
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
```

### 3. Install dependencies
```bash
pip install requests schedule python-dotenv beautifulsoup4
```

### 4. Create .env file
```
SENDER_EMAIL=your@gmail.com
APP_PASSWORD=your_gmail_app_password
RECEIVER_EMAIL=your@gmail.com
```

> Get your Gmail App Password from [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

### 5. Run manually
```bash
python agent.py --now
```

### 6. Run the scheduler (7 AM daily)
```bash
python agent.py
```

---

## ☁️ Cloud Automation (GitHub Actions)

The workflow runs automatically at **7:00 AM IST (1:30 AM UTC)** every day for free.

Add these 3 secrets to your GitHub repo under **Settings → Secrets and variables → Actions:**

| Secret | Value |
|---|---|
| `SENDER_EMAIL` | Your Gmail address |
| `APP_PASSWORD` | Your Gmail App Password |
| `RECEIVER_EMAIL` | Your Gmail address |

---

## 📰 News Categories

| Category | Source |
|---|---|
| 🇮🇳 Top India News | Google News RSS |
| 💼 Business & Economy | Google News RSS |
| 🏏 IPL & Cricket | Google News RSS |
| 💻 Technology | Google News RSS |
| 🏅 Sports | Google News RSS |

---

## 🔐 Security

- Credentials are stored in `.env` locally (never committed to Git)
- Cloud credentials stored in GitHub Secrets (encrypted)
- `.gitignore` blocks `.env` and `venv` from being uploaded

---

## 🧠 What I Learned

- Python automation and scripting
- Working with RSS feeds and XML parsing
- Sending HTML emails programmatically with smtplib
- GitHub Actions for CI/CD and cron scheduling
- Secure credential management with GitHub Secrets
- Debugging Python version conflicts and Windows environment issues

---

## 👤 Author

**Maaz Patwekar**  
[LinkedIn](www.linkedin.com/in/maaz-patwekar) · [GitHub](https://github.com/nullpc)

---

## ⭐ Support

If you found this useful, consider giving it a star on GitHub! ⭐
