import streamlit as st

st.set_page_config(page_title="Groovify", page_icon="🎵", layout="wide")

pages = [
    st.Page("pages/home/home.py", title="Home", icon="🏠"),
    st.Page("pages/finance/finance.py", title="Finance", icon="💰"),
    st.Page("pages/customers/customers.py", title="Customers", icon="👥"),
    st.Page("pages/music/music.py", title="Music Analytics", icon="🎵"),
    st.Page("pages/employees/employees.py", title="Employees", icon="👔"),
    st.Page("pages/alerts/alerts.py", title="Alerts", icon="🚨"),
    st.Page("pages/sql/sql_explorer.py", title="SQL Explorer", icon="🗄️"),
]

nav = st.navigation(pages)
nav.run() 