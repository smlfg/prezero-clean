"""03 – Locations: Messfrequenz, Top-overfull-Standorte."""

from pathlib import Path

from prezero_clean.load import load_fill_levels, load_locations

ROOT = Path(__file__).resolve().parents[1]
FILL = ROOT / "data/raw/glass_fill_levels_anonymized_f.csv"
LOCS = ROOT / "data/external/locations.csv"

df = load_fill_levels(FILL)
locs = load_locations(LOCS)

# Messungen pro Location
counts = df.groupby("Location_id").size().rename("n_measurements")
overfull = df.groupby("Location_id")["overfull"].sum().rename("n_overfull")
agg = counts.to_frame().join(overfull).fillna(0)
agg["overfull_rate"] = (agg["n_overfull"] / agg["n_measurements"]).round(4)

print("Locations gesamt:", len(locs))
print("Locations mit Messungen:", len(agg))
print()
print("Top 10 nach overfull-Rate (min. 3 Messungen):")
top = agg[agg["n_measurements"] >= 3].sort_values("overfull_rate", ascending=False).head(10)
print(top.to_string())
print()
print("Verteilung Messungen pro Location:")
print(counts.describe().round(2).to_string())