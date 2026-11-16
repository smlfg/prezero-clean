"""02 – Auswertung nach Materialtyp (weiß/grün/braun)."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from prezero_clean.load import load_fill_levels
from prezero_clean.eda import by_material

ROOT = Path(__file__).resolve().parents[1]
FILL = ROOT / "data/raw/glass_fill_levels_anonymized_f.csv"
OUT = ROOT / "analyses/outputs"

df = load_fill_levels(FILL)
g = by_material(df)
print(g.to_string())
print()
print("Overfull-Anteil gesamt:", round(float(df["overfull"].mean()), 4))

OUT.mkdir(parents=True, exist_ok=True)
fig, ax = plt.subplots(figsize=(7, 4))
g["overfull_rate"].plot(kind="bar", ax=ax, color=["#f0f0f0", "#2ca02c", "#8c564b"])
ax.set_ylabel("overfull-Rate")
ax.set_title("Overfull-Rate je Material")
fig.tight_layout()
fig.savefig(OUT / "overfull_by_material.png", dpi=120)
plt.close(fig)
print(f"Plot geschrieben nach {OUT / 'overfull_by_material.png'}")