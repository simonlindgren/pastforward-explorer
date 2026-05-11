# PastForward Word Embedding Explorer

Interactive dashboard for exploring Word2Vec models trained on past-related
political Facebook posts from four Nordic countries (Denmark, Finland, Norway,
Sweden), built for the PastForward research project.

**Live dashboard:** https://digsum-pastforward.streamlit.app/

## What it shows

- **The Hindsight Dictionary** — all dictionary terms with translations across
  four languages, grouped by super-category
- **Term frequencies** — which dictionary terms matched the most posts, by country
- **Category breakdown** — super-category distribution by country
- **3D embedding space** — interactive 3D projection of each country's
  Word2Vec model vocabulary

## Running locally

```bash
pip install -r requirements.txt
streamlit run Home.py
```

## Project

Part of the PastForward project at DIGSUM, Umeå University.
