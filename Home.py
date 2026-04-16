import streamlit as st

from lib.header import render_footer, render_header

st.set_page_config(
    page_title="pastforward explorer",
    page_icon="👾",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_header()

# Stats overview
st.markdown(
    """
    <div style="display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 24px;">
        <div style="background: #141414; border: 1px solid #222; border-radius: 8px;
                    padding: 16px 20px; flex: 1; min-width: 140px;">
            <div style="font-size: 0.75em; color: #888; text-transform: uppercase;
                        letter-spacing: 0.5px;">Countries</div>
            <div style="font-size: 1.2em; font-weight: 700; color: #c084fc;
                        margin-top: 8px;">4</div>
        </div>
        <div style="background: #141414; border: 1px solid #222; border-radius: 8px;
                    padding: 16px 20px; flex: 1; min-width: 140px;">
            <div style="font-size: 0.75em; color: #888; text-transform: uppercase;
                        letter-spacing: 0.5px;">Facebook Pages</div>
            <div style="font-size: 1.2em; font-weight: 700; color: #c084fc;
                        margin-top: 8px;">68</div>
        </div>
        <div style="background: #141414; border: 1px solid #222; border-radius: 8px;
                    padding: 16px 20px; flex: 1; min-width: 140px;">
            <div style="font-size: 0.75em; color: #888; text-transform: uppercase;
                        letter-spacing: 0.5px;">Total Posts</div>
            <div style="font-size: 1.2em; font-weight: 700; color: #c084fc;
                        margin-top: 8px;">26,388</div>
        </div>
        <div style="background: #141414; border: 1px solid #222; border-radius: 8px;
                    padding: 16px 20px; flex: 1; min-width: 140px;">
            <div style="font-size: 0.75em; color: #888; text-transform: uppercase;
                        letter-spacing: 0.5px;">Past-Related Posts</div>
            <div style="font-size: 1.2em; font-weight: 700; color: #c084fc;
                        margin-top: 8px;">4,583 (17.4%)</div>
        </div>
        <div style="background: #141414; border: 1px solid #222; border-radius: 8px;
                    padding: 16px 20px; flex: 1; min-width: 140px;">
            <div style="font-size: 0.75em; color: #888; text-transform: uppercase;
                        letter-spacing: 0.5px;">Dictionary Terms</div>
            <div style="font-size: 1.2em; font-weight: 700; color: #c084fc;
                        margin-top: 8px;">61</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Navigation
st.markdown(
    """
    <div style="background: #141414; border: 1px solid #222; border-radius: 8px;
                padding: 20px 24px;">
        <h3 style="font-size: 0.9em; color: #888; text-transform: uppercase;
                   letter-spacing: 0.5px; margin-bottom: 12px;">Explore</h3>
        <div style="font-size: 0.92em; line-height: 2;">
            <span style="color: #c084fc;">›</span>
            <strong>The Hindsight Dictionary</strong>
            <span style="color: #888;"> — All terms with translations across four languages</span><br>
            <span style="color: #c084fc;">›</span>
            <strong>Term Frequencies</strong>
            <span style="color: #888;"> — Which dictionary terms matched the most posts</span><br>
            <span style="color: #c084fc;">›</span>
            <strong>Category Breakdown</strong>
            <span style="color: #888;"> — Super-category distribution by country</span><br>
            <span style="color: #c084fc;">›</span>
            <strong>Similar Terms</strong>
            <span style="color: #888;"> — Word2Vec neighbours of dictionary terms</span><br>
            <span style="color: #c084fc;">›</span>
            <strong>3D Embedding Space</strong>
            <span style="color: #888;"> — Interactive 3D visualisation of model vocabulary</span><br>
            <span style="color: #c084fc;">›</span>
            <strong>About</strong>
            <span style="color: #888;"> — Project background and methodology</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<p style='text-align: center; color: #555; font-size: 0.8em; margin-top: 24px;'>"
    "Select a page from the sidebar to begin.</p>",
    unsafe_allow_html=True,
)

render_footer()
