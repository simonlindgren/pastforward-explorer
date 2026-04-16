"""Page 4: Similar Terms — most similar terms to a dictionary entry in the Word2Vec models."""

import streamlit as st

from lib.data import (
    COUNTRIES,
    COUNTRY_FLAGS,
    COUNTRY_NAMES,
    get_neighbours,
    load_model,
    word_in_vocab,
)
from lib.dictionary import (
    SUPERCATEGORY_COLOURS,
    SUPERCATEGORY_ORDER,
    get_terms_for_country,
)

from lib.header import render_footer, render_header

st.set_page_config(page_title="pastforward explorer", page_icon="👾", layout="wide")
render_header()


def main():
    st.title("Most Similar Terms")
    st.markdown(
        "Select a dictionary term and see what words the Word2Vec model places "
        "closest to it. These are words that appear in similar contexts in the "
        "past-related Facebook posts."
    )

    # Country selector
    country = st.selectbox(
        "Country",
        COUNTRIES,
        format_func=lambda c: f"{COUNTRY_FLAGS[c]} {COUNTRY_NAMES[c]}",
    )

    model = load_model(country)
    terms_map = get_terms_for_country(country)

    # Group terms by super-category, filter to those in vocab
    grouped = {}
    for term, cat in terms_map.items():
        lookup = term.lower().rstrip("*").rstrip("-")
        if word_in_vocab(model, lookup):
            grouped.setdefault(cat, []).append(term)

    # Build a flat list for the selectbox, grouped by category
    term_options = []
    term_labels = {}
    for cat in SUPERCATEGORY_ORDER:
        terms = sorted(grouped.get(cat, []))
        for t in terms:
            term_options.append(t)
            term_labels[t] = f"{t}  [{cat}]"

    if not term_options:
        st.warning(f"No dictionary terms found in the {COUNTRY_NAMES[country]} model vocabulary.")
        return

    selected = st.selectbox(
        "Dictionary term",
        term_options,
        format_func=lambda t: term_labels[t],
    )

    if not selected:
        return

    lookup = selected.lower().rstrip("*").rstrip("-")
    cat = terms_map.get(selected, "Unknown")
    colour = SUPERCATEGORY_COLOURS.get(cat, "#888")

    st.markdown(
        f"<h2 style='color:{colour}; margin-bottom:0;'>{selected}</h2>",
        unsafe_allow_html=True,
    )
    st.caption(f"{cat} · {COUNTRY_FLAGS[country]} {COUNTRY_NAMES[country]}")

    # Number of neighbours
    topn = st.slider("Number of neighbours", min_value=5, max_value=50, value=20)

    neighbours = get_neighbours(model, lookup, topn=topn)

    st.markdown("#### Nearest neighbours (cosine similarity)")

    for word, score in neighbours:
        col1, col2, col3 = st.columns([2, 1, 4])
        with col1:
            st.markdown(word)
        with col2:
            st.markdown(f"`{score:.3f}`")
        with col3:
            st.progress(score, text="")

    # Compare same term across countries
    st.markdown("---")
    st.markdown("#### Same term in other countries")
    st.caption(
        "Looking for the same word (or closest match) in the other countries' models."
    )

    other_countries = [c for c in COUNTRIES if c != country]
    cols = st.columns(len(other_countries))

    for i, other_cc in enumerate(other_countries):
        with cols[i]:
            st.markdown(f"**{COUNTRY_FLAGS[other_cc]} {COUNTRY_NAMES[other_cc]}**")
            other_model = load_model(other_cc)
            other_terms = get_terms_for_country(other_cc)

            # Find equivalent terms in the other country's dictionary
            # that share the same super-category
            found = False
            for ot, ot_cat in other_terms.items():
                if ot_cat != cat:
                    continue
                ot_lookup = ot.lower().rstrip("*").rstrip("-")
                if word_in_vocab(other_model, ot_lookup):
                    st.caption(f"*{ot}*")
                    other_neighbours = get_neighbours(other_model, ot_lookup, topn=5)
                    for w, s in other_neighbours:
                        st.markdown(f"{w} (`{s:.2f}`)")
                    found = True
                    break

            if not found:
                st.caption("No equivalent term in vocabulary")


main()
render_footer()
