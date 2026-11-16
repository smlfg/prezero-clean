"""Laden und Validieren der Rohdaten."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_FILL_COLS = ["Location_id", "material_type", "date", "fill_level_perc"]
REQUIRED_LOC_COLS = ["Location_id", "lat", "lon", "source", "confidence"]


def _normalize_level(value) -> float | None:
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered == "overfull":
            return 110.0
        try:
            return float(lowered)
        except ValueError:
            return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _check_columns(df: pd.DataFrame, required: list[str], name: str) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{name}: fehlende Spalten {missing}")


def load_fill_levels(path: str | Path) -> pd.DataFrame:
    """Lade die Fuellstandsmessungen.

    - Liest CSV (BOM-sicher).
    - Prueft Pflichtspalten.
    - Parst `date` als datetime.
    - Fuegt `overfull` (fill_level_perc >= 100) hinzu.
    """
    path = Path(path)
    df = pd.read_csv(path, encoding="utf-8-sig")
    _check_columns(df, REQUIRED_FILL_COLS, "fill_levels")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # "overfull" ist ein Sonderwert im CSV (kein Prozent). -> 110.0 + Flag.
    df["overfull"] = (
        df["fill_level_perc"].astype(str).str.strip().str.lower() == "overfull"
    )
    df["fill_level_numeric"] = df["fill_level_perc"].map(_normalize_level)
    return df


def load_locations(path: str | Path) -> pd.DataFrame:
    """Lade die Location-Zuordnung (lat/lon + Quelle/Konfidenz)."""
    path = Path(path)
    df = pd.read_csv(path, encoding="utf-8-sig")
    _check_columns(df, REQUIRED_LOC_COLS, "locations")
    return df


def validate_fill_levels(df: pd.DataFrame) -> dict[str, int]:
    """Einfache Datenqualitaets-Pruefung. Gibt Zaehler zurueck."""
    return {
        "rows": len(df),
        "locations": df["Location_id"].nunique(),
        "null_location": int(df["Location_id"].isna().sum()),
        "null_date": int(df["date"].isna().sum()),
        "null_fill": int(df["fill_level_perc"].isna().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "overfull": int(df["overfull"].sum()),
        "materials": int(df["material_type"].nunique()),
    }