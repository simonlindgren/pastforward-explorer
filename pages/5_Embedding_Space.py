"""Page 3: 3D Embedding Space — interactive plotly scatter."""

import json
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from lib.data import (
    COUNTRIES,
    COUNTRY_FLAGS,
    COUNTRY_NAMES,
    POSITION_COLOURS,
    get_precomputed_neighbours,
    get_word_position_counts,
    load_model,
)
from lib.dictionary import (
    SUPERCATEGORY_COLOURS,
    SUPERCATEGORY_ORDER,
    get_terms_for_country,
)

DATA_DIR = Path(__file__).parent.parent / "data"

from lib.header import render_footer, render_header

st.set_page_config(page_title="pastforward explorer", page_icon="👾", layout="wide")
render_header()


@st.cache_data
def load_umap_data():
    with open(DATA_DIR / "umap_3d.json") as f:
        return json.load(f)


def _classify_word(word, dict_terms_lower, precomputed_neighbours, country):
    """Classify a word as 'dictionary', 'neighbour', or 'vocab'."""
    if word in dict_terms_lower:
        return "dictionary"
    country_data = precomputed_neighbours.get(country, {})
    for term, neighbours in country_data.items():
        for nw, _ in neighbours:
            if nw == word:
                return "neighbour"
    return "vocab"


def main():
    st.title("3D Embedding Space")

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        country = st.selectbox(
            "Country",
            COUNTRIES,
            format_func=lambda c: f"{COUNTRY_FLAGS[c]} {COUNTRY_NAMES[c]}",
            key="3d_country",
        )
    with col2:
        colour_by = st.radio(
            "Colour by",
            ["Super-category", "Political position"],
            horizontal=True,
        )
    with col3:
        show_dict = st.checkbox("Dictionary terms", value=True)
        show_neighbours = st.checkbox("Neighbours", value=True)
        show_vocab = st.checkbox("Full vocabulary", value=False)

    umap_data = load_umap_data()
    if country not in umap_data:
        st.error(f"No UMAP data for {COUNTRY_NAMES[country]}.")
        return

    projection = umap_data[country]
    words = projection["words"]
    x = projection["x"]
    y = projection["y"]
    z = projection["z"]

    terms_map = get_terms_for_country(country)
    dict_terms_lower = {t.lower().rstrip("*").rstrip("-") for t in terms_map}
    precomputed = get_precomputed_neighbours()

    categories = []
    word_types = []
    sizes = []
    for w in words:
        wtype = _classify_word(w, dict_terms_lower, precomputed, country)
        word_types.append(wtype)

        cat = None
        for t, c in terms_map.items():
            if t.lower().rstrip("*").rstrip("-") == w:
                cat = c
                break
        categories.append(cat)

        if wtype == "dictionary":
            sizes.append(8)
        elif wtype == "neighbour":
            sizes.append(4)
        else:
            sizes.append(2)

    visible = []
    for i, wt in enumerate(word_types):
        if wt == "dictionary" and show_dict:
            visible.append(i)
        elif wt == "neighbour" and show_neighbours:
            visible.append(i)
        elif wt == "vocab" and show_vocab:
            visible.append(i)

    if not visible:
        st.warning("No points visible. Enable at least one layer.")
        return

    if colour_by == "Super-category":
        colours = []
        for i in visible:
            cat = categories[i]
            if cat:
                colours.append(SUPERCATEGORY_COLOURS[cat])
            elif word_types[i] == "neighbour":
                colours.append("rgba(150, 150, 150, 0.4)")
            else:
                colours.append("rgba(80, 80, 80, 0.2)")
    else:
        word_positions = get_word_position_counts(country)
        colours = []
        for i in visible:
            w = words[i]
            pos_counts = word_positions.get(w, {})
            if pos_counts:
                majority = max(pos_counts, key=pos_counts.get)
                colours.append(POSITION_COLOURS.get(majority, "rgba(80, 80, 80, 0.3)"))
            else:
                colours.append("rgba(80, 80, 80, 0.2)")

    hover = []
    for i in visible:
        w = words[i]
        cat = categories[i] or "—"
        wt = word_types[i]
        hover.append(f"{w}<br>Type: {wt}<br>Category: {cat}")

    text_labels = []
    for i in visible:
        if word_types[i] == "dictionary":
            text_labels.append(words[i])
        else:
            text_labels.append("")

    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=[x[i] for i in visible],
                y=[y[i] for i in visible],
                z=[z[i] for i in visible],
                mode="markers+text",
                marker=dict(
                    size=[sizes[i] for i in visible],
                    color=colours,
                    opacity=0.8,
                    line=dict(width=0),
                ),
                text=text_labels,
                textposition="top center",
                textfont=dict(size=8, color="white"),
                hovertext=hover,
                hoverinfo="text",
            )
        ]
    )

    fig.update_layout(
        scene=dict(
            bgcolor="#0d0d0d",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ),
        paper_bgcolor="#0d0d0d",
        margin=dict(l=0, r=0, t=0, b=0),
        height=700,
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.sidebar:
        st.markdown("### Legend")
        if colour_by == "Super-category":
            for cat in SUPERCATEGORY_ORDER:
                c = SUPERCATEGORY_COLOURS[cat]
                st.markdown(
                    f"<span style='color:{c};'>●</span> {cat}",
                    unsafe_allow_html=True,
                )
            st.markdown(
                "<span style='color:#999;'>●</span> Neighbour",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<span style='color:#555;'>●</span> Other vocabulary",
                unsafe_allow_html=True,
            )
        else:
            for pos, c in POSITION_COLOURS.items():
                st.markdown(
                    f"<span style='color:{c};'>●</span> {pos}",
                    unsafe_allow_html=True,
                )

        st.markdown("### Point size")
        st.markdown("● Large = dictionary term")
        st.markdown("● Medium = semantic neighbour")
        st.markdown("● Small = other vocabulary")

        model = load_model(country)
        st.markdown("### Model stats")
        st.markdown(f"Vocabulary: {len(model.wv):,}")
        st.markdown(f"Dictionary terms: {len(dict_terms_lower)}")
        st.markdown("Dimensions: 100 → 3")
        st.markdown("Projection: UMAP")


main()
render_footer()
