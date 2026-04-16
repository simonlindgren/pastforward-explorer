"""Page 6: About — project background and methodology."""

import streamlit as st

from lib.header import render_footer, render_header

st.set_page_config(page_title="pastforward explorer", page_icon="👾", layout="wide")
render_header()

st.title("About This Dashboard")

st.markdown("""
## The PastForward Project

This dashboard explores Word2Vec models trained on past-related political Facebook
posts from four Nordic countries: Denmark, Finland, Norway, and Sweden. The data was
collected as part of the PastForward research project, which investigates how political
parties and leaders invoke the past in social media election campaigns.

## Data Collection

- **68 Facebook pages** (official party and party leader pages) across all parliamentary
  parties in the four countries
- **26,388 posts** and **215,058 first-level comments** collected via the Meta Content
  Library
- **12-month collection window** per country, ending on election day:
  - Denmark: 2022-11-01
  - Finland: 2023-04-02
  - Norway: 2021-09-13
  - Sweden: 2022-09-11

## The Hindsight Dictionary

A custom dictionary of 61 English-language seed terms in three categories:

- **Conceptual terms** (e.g., memory, tradition, heritage, nostalgia)
- **Temporal markers** (e.g., past, decade, century, "years ago")
- **Phrasal expressions** (e.g., "bring back", "old days", "in hindsight")

These were collaboratively translated and expanded into Danish (96 entries), Finnish
(126), Norwegian (95), and Swedish (187). Posts matching one or more dictionary terms
were classified as "past-related": **4,583 posts (17.4%)**.

## Word2Vec Models

One Word2Vec model was trained per country on the dictionary-matched posts.

**Parameters:**
- Vector dimensionality: 100
- Context window: 5 words
- Minimum word frequency: 3
- Training epochs: 50
- Preprocessing: lowercased, stopwords removed (language-specific lists), multi-word
  names joined (e.g., "Olof Palme" → olof_palme)

**Why these settings?**
- **Separate models per country** capture country-specific discourse rather than
  blending four different political cultures.
- **100 dimensions** balances expressiveness with the relatively small corpus size.
- **50 epochs** (vs. the default 5) gives the model more passes over a small corpus
  to learn stable word representations.

## Composite Scoring

For each dictionary term, the 20 nearest neighbours by cosine similarity are retrieved.
Only neighbours connected to 2+ dictionary terms are retained. The composite score is:

> **(number of connected dictionary terms) x (mean cosine similarity)**

This rewards breadth of connection over incidental similarity to a single entry.

## Team

Samuel Merrill, Simon Lindgren, Manuel Menke, Kalle Eriksson, Karoline Andrea Ihlebæk,
Katarina Pettersson, Marie Meier.

""")

render_footer()
