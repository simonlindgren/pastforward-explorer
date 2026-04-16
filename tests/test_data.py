import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.data import (
    load_model,
    get_neighbours,
    get_precomputed_neighbours,
    load_position_map,
    COUNTRIES,
    COUNTRY_NAMES,
    COUNTRY_FLAGS,
)


def test_countries_constant():
    assert COUNTRIES == ["DK", "FI", "NO", "SE"]


def test_country_names():
    assert COUNTRY_NAMES["DK"] == "Denmark"
    assert COUNTRY_NAMES["SE"] == "Sweden"


def test_load_model_returns_model():
    model = load_model("DK")
    assert model is not None
    assert hasattr(model, "wv")


def test_load_model_has_vocabulary():
    model = load_model("DK")
    assert len(model.wv) > 100


def test_get_neighbours_returns_list():
    model = load_model("DK")
    some_word = list(model.wv.key_to_index.keys())[0]
    neighbours = get_neighbours(model, some_word, topn=5)
    assert isinstance(neighbours, list)
    assert len(neighbours) == 5
    assert isinstance(neighbours[0], tuple)
    assert isinstance(neighbours[0][0], str)
    assert isinstance(neighbours[0][1], float)


def test_get_neighbours_missing_word():
    model = load_model("DK")
    neighbours = get_neighbours(model, "xyznonexistent", topn=5)
    assert neighbours == []


def test_get_precomputed_neighbours():
    data = get_precomputed_neighbours()
    assert "DK" in data
    assert isinstance(data["DK"], dict)
    first_term = next(iter(data["DK"]))
    assert isinstance(data["DK"][first_term], list)
    assert isinstance(data["DK"][first_term][0][1], float)


def test_load_position_map():
    pmap = load_position_map()
    assert isinstance(pmap, dict)
    assert len(pmap) > 0
    sample_val = next(iter(pmap.values()))
    assert sample_val in ("Left", "Centre", "Right")
