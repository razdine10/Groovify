<p align="center">
  <a href="https://groovify.streamlit.app">
    <img src="assets/img/groovify-logo.png" alt="Groovify logo" width="140" />
  </a>
</p>

## 🎵 Groovify — Music & Finance Analytics

A Streamlit app to explore the Chinook database: finance KPIs, customers, employees, music insights, alerts, and a handy SQL explorer.

---

## ✅ Requirements
- Python 3.10+
- A PostgreSQL database (Supabase / Railway / ElephantSQL / local)
- (Optional) A GitHub account if you want to deploy on Streamlit Community Cloud

---

## 🚀 Run locally
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

## ☁️ Deploy on Streamlit Community Cloud (free)
1) Push this project to a new GitHub repo on the `main` branch.
2) Go to `https://share.streamlit.io`, create a new app, and select your repo.
3) Set the entry point to `app.py` (Python 3.10/3.11).
4) Add the environment variables below, then deploy.

---

## 🔐 Environment variables
- `DB_HOST`
- `DB_PORT` (e.g., `5432`)
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

If your provider requires SSL (e.g., Supabase), enable it or add `?sslmode=require` to the connection string.

---

## 📁 Project structure
```
app.py                  # Entry point
assets/                 # CSS + images
pages/                  # Finance, Customers, Employees, Music, Alerts, SQL
src/                    # Utils, queries, shared UI
.streamlit/config.toml  # Theme
config.py               # App config (env-ready)
requirements.txt        # Dependencies
```

---

## 📄 Credits
© Razdine Said — Groovify Analytics. Built with Streamlit, Pandas, Plotly, and PostgreSQL. 