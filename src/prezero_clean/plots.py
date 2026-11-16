"""Einfache Visualisierungen (matplotlib)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_fill_hist(df: pd.DataFrame, out: str | Path | None = None) -> None:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["fill_level_numeric"], bins=20, color="#4C78A8", edgecolor="white")
    ax.set_xlabel("Fuellstand (%)")
    ax.set_ylabel("Messungen")
    ax.set_title("Verteilung der Fuellstaende")
    fig.tight_layout()
    if out is not None:
        fig.savefig(out, dpi=120)
    plt.close(fig)


def plot_overfull_by_month(df: pd.DataFrame, out: str | Path | None = None) -> None:
    monthly = df.assign(month=df["date"].dt.to_period("M").astype(str)).groupby("month")["overfull"].mean()
    fig, ax = plt.subplots(figsize=(10, 4))
    monthly.plot(kind="bar", ax=ax, color="#E45756")
    ax.set_ylabel("overfull-Rate")
    ax.set_title("Overfull-Rate pro Monat")
    fig.tight_layout()
    if out is not None:
        fig.savefig(out, dpi=120)
    plt.close(fig)