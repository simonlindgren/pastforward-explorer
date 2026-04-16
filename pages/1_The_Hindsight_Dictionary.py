"""Page 1: The Hindsight Dictionary — full dictionary overview table."""

import pandas as pd
import streamlit as st

from lib.dictionary import (
    SUPERCATEGORY_COLOURS,
    SUPERCATEGORY_ORDER,
    get_supercategory,
    load_dictionary,
)

from lib.header import render_footer, render_header

st.set_page_config(page_title="pastforward explorer", page_icon="👾", layout="wide")
render_header()


@st.cache_data
def _load_dict_df():
    df = load_dictionary()
    df = df.copy()
    df["Super-category"] = df["English"].apply(get_supercategory)
    df = df[df["Super-category"].notna()].reset_index(drop=True)
    return df


def main():
    st.title("The Hindsight Dictionary")
    st.markdown(
        "The collaboratively-built multilingual term list used to identify "
        "past-oriented discourse in Nordic political Facebook posts. "
        "All 61 English seed terms with their translations in four languages, "
        "grouped by super-category."
    )

    df = _load_dict_df()

    for cat in SUPERCATEGORY_ORDER:
        colour = SUPERCATEGORY_COLOURS[cat]
        cat_df = df[df["Super-category"] == cat].copy()
        if cat_df.empty:
            continue

        count = len(cat_df)
        st.markdown(
            f"<h4 style='color:{colour}; margin-bottom:4px;'>"
            f"● {cat} <span style='font-weight:normal; font-size:0.85em;'>({count} terms)</span>"
            f"</h4>",
            unsafe_allow_html=True,
        )

        rows = []
        for _, row in cat_df.iterrows():
            rows.append({
                "English seed": row["English"],
                "Danish": row["Danish Word(s)"] if pd.notna(row.get("Danish Word(s)")) else "",
                "Finnish": row["Finnish Word(s)"] if pd.notna(row.get("Finnish Word(s)")) else "",
                "Norwegian": row["Norwegian Word(s)"] if pd.notna(row.get("Norwegian Word(s)")) else "",
                "Swedish": row["Swedish Word(s)"] if pd.notna(row.get("Swedish Word(s)")) else "",
            })
        table = pd.DataFrame(rows)
        st.dataframe(table, use_container_width=True, hide_index=True)
        st.markdown("")


main()
render_footer()
