"""Explorative Datenanalyse (Basis)."""

from __future__ import annotations

import pandas as pd


def summary(df: pd.DataFrame) -> pd.Series:
    """Kurze Zusammenfassung der Fuellstandsmessungen."""
    return pd.Series(
        {
            "rows": len(df),
            "locations": df["Location_id"].nunique(),
            "date_min": df["date"].min(),
            "date_max": df["date"].max(),
            "fill_mean": round(float(df["fill_level_numeric"].mean()), 2),
            "fill_median": float(df["fill_level_numeric"].median()),
            "overfull": int(df["overfull"].sum()),
            "overfull_rate": round(float(df["overfull"].mean()), 4),
        }
    )


def by_material(df: pd.DataFrame) -> pd.DataFrame:
    """Fuellstand und overfull-Rate je Materialtyp."""
    g = df.groupby("material_type", dropna=False).agg(
        rows=("fill_level_numeric", "size"),
        fill_mean=("fill_level_numeric", "mean"),
        overfull=("overfull", "sum"),
    )
    g["overfull_rate"] = (g["overfull"] / g["rows"]).round(4)
    return g.sort_values("rows", ascending=False)