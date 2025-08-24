## 🎵 Groovify — Music & Finance Analytics

A simple Streamlit app to explore the Chinook music database: finance KPIs, customers, employees, music insights, alerts, and a handy SQL explorer.

---

## ✅ What you need
- A GitHub account
- A PostgreSQL database (Supabase / Railway / ElephantSQL work great)
- Python 3.10+

---

## 🚀 Deploy for free on Streamlit Community Cloud (Option 1)

Follow this once and your app will auto‑update on every push.

### 1) Put the code on GitHub
```bash
git init
git add .
git commit -m "Groovify initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/groovify.git
git push -u origin main
```

### 2) Create the app on Streamlit Cloud
- Go to `https://share.streamlit.io`
- Click “New app” → pick your repo and branch
- Set the entry point to `app.py`
- Python version: 3.10 or 3.11
- Click “Deploy”

### 3) Add your database credentials (very important)
In your app settings on Streamlit Cloud → “Advanced settings” → “Environment variables”, add:
- `DB_HOST`
- `DB_PORT` (e.g. `5432`)
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

Tip: if your provider requires SSL (Supabase does), add `?sslmode=require` to your connection string or enable SSL in your DB service. If you’re not sure, check your provider’s connection page.

That’s it. Your app will build, run, and get a public URL.

---

## 🧪 Run locally
```bash
pip install -r requirements.txt
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=chinook
export DB_USER=your_user
export DB_PASSWORD=your_password
streamlit run app.py
```

---

## 🧰 Troubleshooting (quick answers)
- “ModuleNotFoundError”: check `requirements.txt` is complete, then redeploy
- “psycopg2 not found”: we ship `psycopg2-binary` — make sure it’s in `requirements.txt`
- “Could not connect to server”: verify DB host/port/credentials, allow public access or add IP allowlist for Streamlit Cloud
- “SSL required”: add `?sslmode=require` to the DB connection (depends on your provider)
- App boots but no data: confirm your database has the Chinook schema and some sample data

---

## 📁 Project layout (short version)
```
app.py                  # Entry point
assets/                 # CSS + images
pages/                  # Finance, Customers, Employees, Music, Alerts, SQL
src/                    # utils, queries, shared UI
.streamlit/config.toml  # Theme
config.py               # App config (env-ready)
requirements.txt        # Dependencies
```

---

## 📄 Credits
© Razdine Said — Groovify Analytics. Built with Streamlit, Pandas, Plotly, and PostgreSQL. 