"""UI components for Groovify application.

This module contains reusable UI components such as the sidebar logo,
custom CSS styling, and other interface elements.
"""

import base64
import os
from datetime import datetime

import streamlit as st


def _load_logo_base64() -> str:
    """Try multiple common paths to find the Groovify logo.
    
    Returns:
        Base64 encoded string of the logo image, empty string if not found
    """
    candidate_paths = [
        "assets/img/groovify-logo.png",
        "assets/img/groovify_logo.png", 
        "assets/img/logo.png",
        "assets/groovify-logo.png",
        "assets/groovify_logo.png",
        "groovify-logo.png",
        "assets/logo.png",
    ]
    
    for path in candidate_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            except Exception:  # noqa: BLE001
                continue
    return ""


def apply_sidebar_logo():
    """Render the round Groovify logo fixed at bottom of sidebar."""
    logo_base64 = _load_logo_base64()

    if logo_base64:
        st.markdown(
            f"""
        <style>
        [data-testid="stSidebar"] {{ position: relative; }}
        [data-testid="stSidebar"]::after {{
            content: "";
            position: fixed;
            bottom: 20px;
            left: 90px;
            width: 60px;
            height: 60px;
            background-image: url("data:image/png;base64,{logo_base64}");
            background-size: 60px 60px;
            background-repeat: no-repeat;
            background-position: center;
            background-color: rgba(255,255,255,0.95);
            border-radius: 50%;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            z-index: 1000;
            transition: transform 0.2s ease;
            border: 2px solid rgba(0,0,0,0.05);
        }}
        [data-testid="stSidebar"]::after:hover {{ 
            transform: scale(1.06); 
        }}

        @media (max-width: 768px) {{
            [data-testid="stSidebar"]::after {{ display: none; }}
        }}
        </style>
        """,
            unsafe_allow_html=True,
        )
    else:
        # Fallback minimal emoji badge at bottom
        st.sidebar.markdown(
            """
            <style>
            [data-testid='stSidebar']{ position:relative; }
            .groovify-fallback{ 
                position:absolute; 
                bottom:16px; 
                left:50%; 
                transform:translateX(-50%); 
                width:56px; 
                height:56px; 
                border-radius:50%; 
                background:rgba(255,255,255,0.95); 
                box-shadow:0 4px 15px rgba(0,0,0,0.15); 
                display:flex; 
                align-items:center; 
                justify-content:center; 
                border:2px solid rgba(0,0,0,0.05); 
            }
            @media (max-width:768px){ 
                .groovify-fallback{ display:none; } 
            }
            </style>
            <div class='groovify-fallback'>🎵</div>
            """,
            unsafe_allow_html=True,
        )


def render_footer() -> None:
    """Render a professional footer with copyright and timestamp."""
    current_year = datetime.now().year
    timestamp = datetime.now().strftime("%d %b %Y • %H:%M")
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align:center; color:#6b7280; font-size: 0.9rem;">
            © {current_year} Razdine Said • Groovify Analytics • Last update: {timestamp}
        </div>
        """,
        unsafe_allow_html=True,
    ) 