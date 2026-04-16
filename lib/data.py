"""Model loading, neighbour queries, and position mapping."""

import json
from pathlib import Path

import pandas as pd
from gensim.models import Word2Vec

DATA_DIR = Path(__file__).parent.parent / "data"

COUNTRIES = ["DK", "FI", "NO", "SE"]

COUNTRY_NAMES = {
    "DK": "Denmark",
    "FI": "Finland",
    "NO": "Norway",
    "SE": "Sweden",
}

COUNTRY_FLAGS = {
    "DK": "🇩🇰",
    "FI": "🇫🇮",
    "NO": "🇳🇴",
    "SE": "🇸🇪",
}

POSITION_COLOURS = {
    "Left": "#ef4444",
    "Centre": "#f59e0b",
    "Right": "#3b82f6",
}

_models = {}


def load_model(country):
    """Load a gensim Word2Vec model for a country. Cached after first load."""
    if country not in _models:
        path = DATA_DIR / f"w2v_{country}.model"
        _models[country] = Word2Vec.load(str(path))
    return _models[country]


def get_neighbours(model, word, topn=20):
    """Return [(word, similarity), ...] for nearest neighbours. Empty list if word not in vocab."""
    try:
        return model.wv.most_similar(word, topn=topn)
    except KeyError:
        return []


def word_in_vocab(model, word):
    """Check if a word exists in the model's vocabulary."""
    return word in model.wv


def get_vocabulary(model):
    """Return the full vocabulary list for a model."""
    return list(model.wv.key_to_index.keys())


def get_precomputed_neighbours():
    """Load the pre-computed word2vec_similarities.json."""
    path = DATA_DIR / "word2vec_similarities.json"
    with open(path) as f:
        return json.load(f)


def load_position_map():
    """Load page name → political position mapping from table4_account_detail.csv."""
    path = DATA_DIR / "table4_account_detail.csv"
    df = pd.read_csv(path)
    return dict(zip(df["Account"], df["Position"]))


def load_filtered_posts():
    """Load pf-filtered-posts.json as a list of dicts."""
    path = DATA_DIR / "pf-filtered-posts.json"
    with open(path) as f:
        return json.load(f)


def get_word_position_counts(country):
    """For each word in a country's filtered posts, count occurrences by position.

    Returns {word: {"Left": n, "Centre": n, "Right": n}}.
    Requires pre-computed word_positions.json (built by prepare_data.py).
    """
    path = DATA_DIR / "word_positions.json"
    with open(path) as f:
        all_data = json.load(f)
    return all_data.get(country, {})
