"""Shared DIGSUM header banner for all pages."""

import base64
from pathlib import Path

import streamlit as st

_LOGO_PATH = Path(__file__).parent.parent / "data" / "digsum-logo.png"

_GH_ICON = (
    '<svg style="width:12px;height:12px;vertical-align:-1px;margin-right:3px" '
    'viewBox="0 0 16 16" fill="#03A1E7"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 '
    "2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53"
    "-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08"
    ".58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89"
    "-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2"
    ".82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44"
    " 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29"
    ".25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 "
    '0016 8c0-4.42-3.58-8-8-8z"/></svg>'
)


def render_header():
    """Render the DIGSUM header bar matching the marina dashboard style."""
    # Scale down default Streamlit font sizes to match the marina dashboard
    st.markdown(
        """
        <style>
            .stMainBlockContainer { font-size: 0.88em; }
            .stMainBlockContainer h1 { font-size: 1.5em; }
            .stMainBlockContainer h2 { font-size: 1.2em; }
            .stMainBlockContainer h3 { font-size: 1.05em; }
            .stMainBlockContainer h4 { font-size: 0.95em; }
            .stMainBlockContainer .stMarkdown p { font-size: 0.92em; }
            .stMainBlockContainer .stDataFrame { font-size: 0.85em; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if _LOGO_PATH.exists():
        logo_b64 = base64.b64encode(_LOGO_PATH.read_bytes()).decode()
        st.markdown(
            f"""
            <div style="background: #000; padding: 24px 30px; border-radius: 0;
                        border-bottom: 1px solid #222; margin: -1rem -1rem 24px -1rem;
                        display: flex; align-items: center; gap: 24px;">
                <div style="flex-shrink: 0;">
                    <img src="data:image/png;base64,{logo_b64}" style="height: 70px;" />
                    <div style="font-size: 0.65em; color: #03A1E7; margin-top: 4px;
                                font-family: monospace; padding-left: 12px;">
                        {_GH_ICON}github.com/simonlindgren
                    </div>
                </div>
                <div>
                    <h1 style="font-size: 1.3em; font-weight: 600; letter-spacing: 1px;
                               text-transform: uppercase; margin: 0;
                               background: linear-gradient(90deg, #c084fc, #f472b6, #4ade80);
                               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        PastForward Explorer
                    </h1>
                    <p style="font-size: 0.85em; color: #777; margin-top: 6px;">
                        Political memory in Nordic Facebook election campaigns · 4 countries · 26,388 posts · 4,583 past-related
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_footer():
    """Render a minimal footer."""
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 40px; padding: 16px;
                    border-top: 1px solid #2a2a2a; color: #555; font-size: 0.75em;">
            {_GH_ICON}
            <a href="https://github.com/simonlindgren" style="color: #03A1E7;
               text-decoration: none;">github.com/simonlindgren</a>
            <span style="margin: 0 8px;">·</span>
            DIGSUM · Umeå University
        </div>
        """,
        unsafe_allow_html=True,
    )
