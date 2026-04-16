"""Dictionary parsing, super-category mapping, and term availability."""

import csv
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

SUPERCATEGORY_ORDER = [
    "Memory/remembrance",
    "Tradition/heritage",
    "Nostalgia/loss",
    "Restoration/return",
    "Temporal markers",
    "Historical reference",
]

SUPERCATEGORY_COLOURS = {
    "Memory/remembrance": "#c084fc",
    "Tradition/heritage": "#4ade80",
    "Nostalgia/loss": "#f97316",
    "Restoration/return": "#38bdf8",
    "Temporal markers": "#f59e0b",
    "Historical reference": "#ef4444",
}

COUNTRY_LANGUAGES = {
    "DK": ("Danish Word(s)", "Danish"),
    "FI": ("Finnish Word(s)", "Finnish"),
    "NO": ("Norwegian Word(s)", "Norwegian"),
    "SE": ("Swedish Word(s)", "Swedish"),
}

_ENGLISH_TO_SUPERCATEGORY = {
    "Memor*": "Memory/remembrance",
    "Commemor*": "Memory/remembrance",
    "Rememb*": "Memory/remembrance",
    "Recollection": "Memory/remembrance",
    "Remind*": "Memory/remembrance",
    "in hindsight": "Memory/remembrance",
    "Tradition*": "Tradition/heritage",
    "Heritage": "Tradition/heritage",
    "Legacy": "Tradition/heritage",
    "Origin*": "Tradition/heritage",
    "Preserve": "Tradition/heritage",
    "before us": "Tradition/heritage",
    "over time": "Tradition/heritage",
    "whole life": "Tradition/heritage",
    "my past": "Tradition/heritage",
    "Nostalgi*": "Nostalgia/loss",
    "Vanished": "Nostalgia/loss",
    "Decay": "Nostalgia/loss",
    "Erosion": "Nostalgia/loss",
    "Better before": "Nostalgia/loss",
    "Worse before": "Nostalgia/loss",
    "old days": "Nostalgia/loss",
    "my youth": "Nostalgia/loss",
    "my childhood": "Nostalgia/loss",
    "grew up": "Nostalgia/loss",
    "Restore": "Restoration/return",
    "Reconstruct": "Restoration/return",
    "Rebuild": "Restoration/return",
    "Recreate": "Restoration/return",
    "Reclaim": "Restoration/return",
    "Return": "Restoration/return",
    "bring back": "Restoration/return",
    "Past": "Temporal markers",
    "Ancient": "Temporal markers",
    "Decade": "Temporal markers",
    "Recent*": "Temporal markers",
    "centur*": "Temporal markers",
    "former*": "Temporal markers",
    "previous*": "Temporal markers",
    "epoch": "Temporal markers",
    "Period": "Temporal markers",
    "Viking": "Temporal markers",
    "Obsolete": "Temporal markers",
    "Bygone": "Temporal markers",
    "years ago": "Temporal markers",
    "years since": "Temporal markers",
    "long time": "Temporal markers",
    "long ago": "Temporal markers",
    "back then": "Temporal markers",
    "Last year": "Temporal markers",
    "Last decade": "Temporal markers",
    "last election*": "Temporal markers",
    "last governmental period": "Temporal markers",
    "Never before": "Temporal markers",
    "four years": "Temporal markers",
    "eight years": "Temporal markers",
    "modern time": "Temporal markers",
    "Histor*": "Historical reference",
    "Generation*": "Historical reference",
}


def load_dictionary():
    """Load dictionary-terms.csv, skipping category header rows."""
    import pandas as pd

    path = DATA_DIR / "dictionary-terms.csv"
    df = pd.read_csv(path)
    df = df.dropna(subset=["English"])
    df = df[~df["English"].str.contains(r"\d+\s*Rows?\)", case=False, na=False)]
    df = df.reset_index(drop=True)
    return df


def get_supercategory(english_term):
    """Return the super-category for an English seed term, or None.

    Matches both exact keys and expanded CSV values (e.g. the key "Memor*"
    will match the CSV cell "Memor*, Memory, Memories, Memorial, ...").
    """
    if english_term in _ENGLISH_TO_SUPERCATEGORY:
        return _ENGLISH_TO_SUPERCATEGORY[english_term]
    term_lower = english_term.lower().strip()
    for key, cat in _ENGLISH_TO_SUPERCATEGORY.items():
        key_lower = key.lower()
        # Exact case-insensitive match
        if key_lower == term_lower:
            return cat
        # Key is a glob stem (e.g. "memor*"): check if the English cell
        # starts with the stem or contains the stem as its first token.
        if key_lower.endswith("*"):
            stem = key_lower.rstrip("*")
            if term_lower.startswith(stem):
                return cat
        # Key is a phrase: check if the English cell starts with the key
        # (handles expanded values like "Tradition*, Tradition, Traditions ...")
        if term_lower.startswith(key_lower):
            return cat
    return None


def get_terms_for_country(country):
    """Return {local_term: supercategory} for all dictionary terms in a country."""
    df = load_dictionary()
    col_name = COUNTRY_LANGUAGES[country][0]
    result = {}

    for _, row in df.iterrows():
        english = row["English"]
        cat = get_supercategory(english)
        if cat is None:
            continue

        cell = row.get(col_name)
        if not isinstance(cell, str) or not cell.strip():
            continue

        for term in cell.split(","):
            term = term.strip().strip('"').strip()
            if term and not term.startswith("("):
                result[term] = cat

    return result


def get_english_gloss(local_term, country):
    """Given a local-language term and country, return the English seed term."""
    df = load_dictionary()
    col_name = COUNTRY_LANGUAGES[country][0]

    for _, row in df.iterrows():
        cell = row.get(col_name)
        if not isinstance(cell, str):
            continue
        terms_in_cell = [t.strip().strip('"').lower() for t in cell.split(",")]
        if local_term.lower() in terms_in_cell:
            return row["English"]
    return None


def get_cross_country_equivalents(english_term):
    """Given an English seed term, return {country: [local_terms]} for all countries."""
    df = load_dictionary()
    result = {}

    for _, row in df.iterrows():
        if row["English"] != english_term:
            continue
        for cc, (col, _) in COUNTRY_LANGUAGES.items():
            cell = row.get(col)
            if isinstance(cell, str) and cell.strip():
                terms = [t.strip().strip('"') for t in cell.split(",") if t.strip()]
                result[cc] = terms
        break

    return result
