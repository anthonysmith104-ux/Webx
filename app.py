"""
Lathrop & Co. — prototype site, served via Streamlit.

Repo layout for deployment:
    your-repo/
    ├── app.py                          <- this file
    ├── contractor-site-prototype.html  <- the prototype
    └── requirements.txt                <- just: streamlit

The HTML is rendered inside a component iframe (not st.markdown) because
st.markdown strips <script> tags, which would kill the quote form,
estimator, and booking interactions.
"""

from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Lathrop & Co. — Painting · Finishing · Remodeling",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Strip all Streamlit chrome + padding so the page fills the screen ---
st.markdown(
    """
    <style>
      #MainMenu, footer {visibility: hidden;}
      header[data-testid="stHeader"] {display: none !important;}
      .stApp {background: #f4efe6;}
      /* kill default page padding/margins */
      .block-container,
      [data-testid="stAppViewContainer"] > .main,
      [data-testid="stMainBlockContainer"] {
          padding: 0 !important;
          margin: 0 !important;
          max-width: 100% !important;
      }
      [data-testid="stVerticalBlock"] {gap: 0 !important;}
      /* make the component iframe fill the viewport; it scrolls internally */
      iframe {
          height: 100vh !important;
          width: 100% !important;
          border: none !important;
          display: block;
      }
      div[data-testid="stIFrame"] {height: 100vh !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Load and render the prototype ---
html_path = Path(__file__).parent / "contractor-site-prototype.html"
html = html_path.read_text(encoding="utf-8")

# height is a fallback; the CSS above stretches it to the full viewport.
# scrolling=True lets the site scroll inside the iframe (keeps the sticky nav working).
components.html(html, height=1000, scrolling=True)
