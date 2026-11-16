from pathlib import Path

import pandas as pd

from prezero_clean.load import load_fill_levels, load_locations, validate_fill_levels

ROOT = Path(__file__).resolve().parents[1]
FILL = ROOT / "data/raw/glass_fill_levels_anonymized_f.csv"
LOCS = ROOT / "data/external/locations.csv"


def test_fill_levels_shape_and_columns():
    df = load_fill_levels(FILL)
    assert len(df) == 11701
    for col in ["Location_id", "material_type", "date", "fill_level_perc", "overfull", "fill_level_numeric"]:
        assert col in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_overfull_count():
    df = load_fill_levels(FILL)
    assert int(df["overfull"].sum()) == 1192


def test_locations_count():
    df = load_locations(LOCS)
    assert len(df) == 449
    assert df["Location_id"].nunique() == 449


def test_validate_reports_expected():
    df = load_fill_levels(FILL)
    v = validate_fill_levels(df)
    assert v["rows"] == 11701
    assert v["locations"] == 449
    assert v["overfull"] == 1192
    assert v["null_location"] == 0
    assert v["null_date"] == 0
    assert v["null_fill"] == 0