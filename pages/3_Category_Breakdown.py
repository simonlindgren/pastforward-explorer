"""Page 3: Category Breakdown — category × country breakdown."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib.data import COUNTRIES, COUNTRY_FLAGS, COUNTRY_NAMES, load_filtered_posts
from lib.dictionary import (
    SUPERCATEGORY_COLOURS,
    SUPERCATEGORY_ORDER,
    get_terms_for_country,
)

from lib.header import render_footer, render_header

st.set_page_config(page_title="pastforward explorer", page_icon="👾", layout="wide")
render_header()


@st.cache_data
def _compute_category_country_matrix():
    posts = load_filtered_posts()

    term_to_cat = {}
    for country in COUNTRIES:
        term_to_cat[country] = {
            t.lower().rstrip("*").rstrip("-"): cat
            for t, cat in get_terms_for_country(country).items()
        }

    matrix = {cat: {c: 0 for c in COUNTRIES} for cat in SUPERCATEGORY_ORDER}

    for post in posts:
        country = post.get("country")
        if country not in COUNTRIES:
            continue
        mt = post.get("matched_terms", "")
        if not mt:
            continue
        country_lookup = term_to_cat[country]
        for term in mt.split(","):
            term = term.strip()
            term_lower = term.lower().rstrip("*").rstrip("-")
            cat = country_lookup.get(term_lower)
            if cat and cat in matrix:
                matrix[cat][country] += 1

    df = pd.DataFrame(matrix).T
    df = df.loc[SUPERCATEGORY_ORDER, COUNTRIES]
    return df


def main():
    st.title("Category Breakdown")
    st.markdown(
        "How many term matches came from each super-category in each country? "
        "This shows which conceptual areas dominate the past-oriented discourse."
    )

    matrix_df = _compute_category_country_matrix()

    chart_type = st.radio(
        "Chart type",
        ["Stacked bar", "Stacked 100%", "Heatmap"],
        horizontal=True,
    )

    country_labels = [f"{COUNTRY_FLAGS[c]} {COUNTRY_NAMES[c]}" for c in COUNTRIES]

    if chart_type in ("Stacked bar", "Stacked 100%"):
        is_pct = chart_type == "Stacked 100%"

        # Compute column totals for percentage mode
        col_totals = {c: sum(matrix_df[c]) for c in COUNTRIES}

        fig = go.Figure()
        for cat in SUPERCATEGORY_ORDER:
            colour = SUPERCATEGORY_COLOURS[cat]
            if is_pct:
                values = [
                    round(100 * matrix_df.loc[cat, c] / col_totals[c], 1)
                    if col_totals[c] > 0 else 0
                    for c in COUNTRIES
                ]
            else:
                values = [matrix_df.loc[cat, c] for c in COUNTRIES]
            fig.add_trace(
                go.Bar(
                    name=cat,
                    x=country_labels,
                    y=values,
                    marker_color=colour,
                    marker_line_width=0,
                )
            )
        fig.update_layout(
            barmode="stack",
            paper_bgcolor="#0d0d0d",
            plot_bgcolor="#0d0d0d",
            font=dict(color="white"),
            xaxis=dict(color="white", gridcolor="#1e1e3a"),
            yaxis=dict(
                title="% of matches" if is_pct else "Match count",
                color="white",
                gridcolor="#1e1e3a",
            ),
            legend=dict(bgcolor="#0d0d0d", bordercolor="#333", borderwidth=1, font=dict(color="white")),
            margin=dict(l=60, r=20, t=20, b=40),
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        z = matrix_df.values.tolist()
        text = [[str(v) for v in row] for row in z]
        fig = go.Figure(
            go.Heatmap(
                z=z,
                x=country_labels,
                y=SUPERCATEGORY_ORDER,
                text=text,
                texttemplate="%{text}",
                colorscale="Blues",
                hoverongaps=False,
                showscale=True,
            )
        )
        fig.update_layout(
            paper_bgcolor="#0d0d0d",
            plot_bgcolor="#0d0d0d",
            font=dict(color="white"),
            xaxis=dict(color="white"),
            yaxis=dict(color="white", autorange="reversed"),
            margin=dict(l=200, r=20, t=20, b=40),
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Show raw counts table"):
        display_df = matrix_df.copy()
        display_df.columns = [f"{COUNTRY_FLAGS[c]} {COUNTRY_NAMES[c]}" for c in COUNTRIES]
        display_df.index.name = "Super-category"
        st.dataframe(display_df, use_container_width=True)


main()
render_footer()
