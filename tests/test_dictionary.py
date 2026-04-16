import pytest
import sys
from pathlib import Path

# Add dashboard dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.dictionary import (
    load_dictionary,
    get_supercategory,
    get_terms_for_country,
    SUPERCATEGORY_ORDER,
    SUPERCATEGORY_COLOURS,
    COUNTRY_LANGUAGES,
)


def test_supercategory_order_has_six_entries():
    assert len(SUPERCATEGORY_ORDER) == 6


def test_supercategory_colours_match_order():
    assert set(SUPERCATEGORY_COLOURS.keys()) == set(SUPERCATEGORY_ORDER)


def test_country_languages_has_four_countries():
    assert set(COUNTRY_LANGUAGES.keys()) == {"DK", "FI", "NO", "SE"}


def test_load_dictionary_returns_dataframe():
    df = load_dictionary()
    assert "English" in df.columns
    assert "Danish Word(s)" in df.columns
    assert len(df) > 50


def test_get_supercategory_known_term():
    cat = get_supercategory("Memor*")
    assert cat == "Memory/remembrance"


def test_get_supercategory_unknown_term():
    cat = get_supercategory("xyznonexistent")
    assert cat is None


def test_get_terms_for_country_returns_dict():
    terms = get_terms_for_country("DK")
    assert isinstance(terms, dict)
    assert len(terms) > 0
    for cat in terms.values():
        assert cat in SUPERCATEGORY_ORDER


def test_get_terms_for_country_danish_has_minde():
    terms = get_terms_for_country("DK")
    lower_terms = {t.lower() for t in terms}
    assert any("mind" in t for t in lower_terms)
