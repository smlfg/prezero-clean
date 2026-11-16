"""01 – Uebersicht der Fuellstandsmessungen."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

from prezero_clean.load import load_fill_levels
from prezero_clean.eda import summary
from prezero_clean.plots import plot_fill_hist, plot_overfull_by_month

ROOT = Path(__file__).resolve().parents[1]
FILL = ROOT / "data/raw/glass_fill_levels_anonymized_f.csv"
OUT = ROOT / "analyses/outputs"

df = load_fill_levels(FILL)
print(summary(df).to_string())
OUT.mkdir(parents=True, exist_ok=True)
plot_fill_hist(df, OUT / "fill_hist.png")
plot_overfull_by_month(df, OUT / "overfull_by_month.png")
print(f"\nPlots geschrieben nach {OUT}")
