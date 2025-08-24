import base64

import streamlit as st

from utils import DB_CONFIG, apply_sidebar_logo


@st.cache_data
def get_logo_base64():
    """Convertir le logo en base64 pour l'affichage HTML."""
    try:
        with open("assets/img/groovify-logo.png", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""


def main() -> None:
    # Appliquer le logo en bas de sidebar
    apply_sidebar_logo()
    
    # CSS personnalisé pour le style
    st.markdown("""
    <style>
    .main-header {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 40px;
        margin-top: 20px;
    }
    .logo-container {
        width: 300px;
        height: 300px;
    }
    .logo-container img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        border-radius: 30px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    .logo-container img:hover {
        transform: scale(1.05);
    }
    .title-container h1 {
        margin: 0;
        color: #2D3748;
        font-size: 3.5rem !important;
        font-weight: bold;
    }
    .title-container .caption {
        margin-top: 8px;
        color: #64748B;
        font-size: 1.3rem;
        font-weight: 500;
    }
    </style>
    """.replace("{logo_base64}", get_logo_base64()), unsafe_allow_html=True)
    
    # Header avec logo énorme
    st.markdown("""
    <div class="main-header">
        <div class="logo-container">
            <img src="data:image/png;base64,{}" alt="Groovify Logo">
        </div>
    </div>
    """.format(get_logo_base64()), unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    ## 🎯 Welcome to Groovify!

    Groovify is a finance-focused application that leverages the Chinook database.
    Originally, Chinook represents an online music store. We use it here as a foundation to analyze financial and business data.

    The information processed covers:
    - 🎵 **Products**: albums and music tracks treated as sold items.
    - 👥 **Customers and purchases**: profiles, segments, loyalty.
    - 💳 **Invoices and transactions**: payments, amounts, payment methods.
    - 🎧 **Playlists**: grouped product/offer sets.
    - 🧑‍💼 **Employees**: internal structure and sales management.
    - 📊 **Financial indicators**: revenue, forecasts, anomalies and reports.

    👉 **In summary**: Groovify transforms the Chinook music database into a financial analysis tool to explore products, customers, sales and overall performance.
    
    **Navigation:** Use the menu in the left sidebar to explore the different sections.
    """)

    with st.sidebar:
        st.markdown("---")
        st.markdown("**🗄️ Database**")
        st.info(f"🐘 PostgreSQL: {DB_CONFIG['database']}")
        st.markdown("**📊 Data source**")
        st.markdown("[Chinook Database (GitHub)](https://github.com/lerocha/chinook-database)")

    from src.utils.ui_components import render_footer
    render_footer()


if __name__ == "__main__":
    main() 