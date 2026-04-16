"""Page 2: Term Frequencies — which dictionary terms matched the most posts."""

from collections import Counter

import plotly.graph_objects as go
import streamlit as st

from lib.data import COUNTRIES, COUNTRY_FLAGS, COUNTRY_NAMES, load_filtered_posts

from lib.header import render_footer, render_header

st.set_page_config(page_title="pastforward explorer", page_icon="👾", layout="wide")
render_header()


@st.cache_data
def _compute_term_counts():
    posts = load_filtered_posts()
    counts = {c: Counter() for c in COUNTRIES}
    for post in posts:
        country = post.get("country")
        if country not in counts:
            continue
        mt = post.get("matched_terms", "")
        if not mt:
            continue
        for term in mt.split(","):
            term = term.strip()
            if term:
                counts[country][term] += 1
    return counts


def _plot_term_bar(counter, top_n, title, height=600):
    if not counter:
        st.warning(f"No matched terms data for {title}.")
        return

    top = counter.most_common(top_n)
    terms = [t for t, _ in top][::-1]
    counts = [c for _, c in top][::-1]

    fig = go.Figure(
        go.Bar(
            x=counts,
            y=terms,
            orientation="h",
            marker_color="#7c3aed",
            marker_line_width=0,
        )
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color="white")),
        paper_bgcolor="#0d0d0d",
        plot_bgcolor="#0d0d0d",
        font=dict(color="white"),
        xaxis=dict(title="Post count", gridcolor="#1e1e3a", color="white"),
        yaxis=dict(tickfont=dict(size=11), color="white"),
        margin=dict(l=160, r=20, t=50, b=40),
        height=height,
    )
    st.plotly_chart(fig, use_container_width=True)


def main():
    st.title("Term Frequencies")
    st.markdown(
        "Which dictionary terms matched the most posts? "
        "Each post may contribute multiple matched terms."
    )

    term_counts = _compute_term_counts()

    col_view, col_n = st.columns([2, 1])
    with col_view:
        view = st.radio(
            "Display",
            ["One country", "All countries side by side"],
            horizontal=True,
        )
    with col_n:
        top_n = st.slider("Top N terms", min_value=5, max_value=40, value=20)

    if view == "One country":
        country = st.selectbox(
            "Country",
            COUNTRIES,
            format_func=lambda c: f"{COUNTRY_FLAGS[c]} {COUNTRY_NAMES[c]}",
        )
        _plot_term_bar(term_counts[country], top_n, COUNTRY_NAMES[country])
    else:
        cols = st.columns(2)
        for i, country in enumerate(COUNTRIES):
            with cols[i % 2]:
                _plot_term_bar(
                    term_counts[country],
                    top_n,
                    f"{COUNTRY_FLAGS[country]} {COUNTRY_NAMES[country]}",
                    height=500,
                )


main()
render_footer()
