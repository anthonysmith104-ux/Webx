"""
Asgard Construction LLC — prototype site, served via Streamlit.

Repo layout for deployment:
    your-repo/
    ├── app.py            <- this file
    ├── asgard-site.html  <- the prototype (favicon is embedded inside it)
    └── requirements.txt  <- streamlit + pillow

The HTML is rendered inside a component iframe (not st.markdown) because
st.markdown strips <script> tags, which would kill the quote form,
estimator, booking, and owner-portal interactions.

The browser-tab icon (page_icon) is pulled straight from the favicon that
is already embedded in asgard-site.html, so there is no separate image
file to keep in sync.
"""

from pathlib import Path
import base64
import io
import re
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

# --- Read the site once; reuse it for both the tab icon and the iframe ---
html = (Path(__file__).parent / "asgard-site.html").read_text(encoding="utf-8")


def _tab_icon(markup):
    """Decode the favicon embedded in the HTML <link rel='icon'> tag."""
    m = re.search(r'rel="icon"[^>]*href="data:image/png;base64,([^"]+)"', markup)
    if m:
        try:
            return Image.open(io.BytesIO(base64.b64decode(m.group(1))))
        except Exception:
            pass
    return "🔨"  # fallback only if the embedded icon can't be read


st.set_page_config(
    page_title="Asgard Construction LLC — Painting · Finishing · Remodeling",
    page_icon=_tab_icon(html),
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
      .block-container,
      [data-testid="stAppViewContainer"] > .main,
      [data-testid="stMainBlockContainer"] {
          padding: 0 !important;
          margin: 0 !important;
          max-width: 100% !important;
      }
      [data-testid="stVerticalBlock"] {gap: 0 !important;}
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

# --- Render the prototype (height is a fallback; CSS stretches it full-height) ---
components.html(html, height=1000, scrolling=True)
