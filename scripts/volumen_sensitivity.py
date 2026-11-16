#!/usr/bin/env python3
"""Volumen-Sensitivity: interne Füllstände (CSV) x externes Kammervolumen.

Operative Annahme A6 (farbabhängig, AGENTS.md §3): white 3,2 / green 2,1 / brown 1,1 m³ je Farb-Behälter.
Vergleichsszenarien: A6-kompakt (3,2/1,89/0,68 m³, gleiche Quelle) und gleichmäßige Kammer (V-1 Bandbreite).
Externe Parameter mit Quellen: docs/externe_parameter.md (V-1, V-2, V-3).
Alle Füllstände sind 'gemessen' (CSV); alle Volumina sind 'modelliert'
(= Ergebnis von A6, nie CSV-Wahrheit). Aufruf: python scripts/volumen_sensitivity.py [pfad_zur_csv]"""
import sys
from pathlib import Path
import pandas as pd

CSV = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "data" / "raw" / "glass_fill_levels_anonymized_f.csv"
d = pd.read_csv(CSV, parse_dates=["date"])

# --- Externe Parameter (docs/externe_parameter.md) ---
# A6 operativ (V-3, IGF 19596 N "intercon"): Bedarfsvolumina je Farbfraktion
A6 = {"white": 3.2, "green": 2.1, "brown": 1.1}
# A6-kompakt (gleiche Quelle, 3-Kammer-Bauform)
A6K = {"white": 3.2, "green": 1.89, "brown": 0.68}
# V-1 gleichmäßige Kammer (Bandbreite, nur Vergleich)
V1 = {"klein": 0.53, "standard": 1.07, "groß": 1.67}

def h(t): print(f"\n== {t}")

h("0 Annahmen")
print("A6 farbabhängig (m³ je Farb-Behälter):", A6, "| Quelle: docs/externe_parameter.md V-3 (IGF 19596 N, Abruf 2026-11-16)")
print("Vergleich: A6-kompakt", A6K, "| V-1 gleichmäßig", V1)
print("overfull = mindestens volle Kammer, genauer Wert unbekannt (A3/V-2) -> alle overfull-Werte sind Untergrenzen")

# --- Interne Füllstände aus der CSV ---
d["ueber"] = d.fill_level_perc.eq("overfull")
d["p"] = pd.to_numeric(d.fill_level_perc.where(~d.ueber))
# Volumenanteil je Messung: Füllstand% / 100, overfull -> Untergrenze 1,0 (V-2)
d["anteil"] = (d.p / 100).where(~d.ueber, 1.0)
print("Messungen:", len(d), "| numerisch:", int((~d.ueber).sum()), "| overfull:", int(d.ueber.sum()))

def farbvol(row, vo):
    """Volumen je Messung = Füllstand-Anteil x Farb-Behältervolumen (modelliert)."""
    return row.anteil * vo[row.material_type]

d["v_a6"] = d.apply(lambda r: farbvol(r, A6), axis=1)
d["v_a6k"] = d.apply(lambda r: farbvol(r, A6K), axis=1)

h("1 Gesamteingesammeltes Volumen je Farbe (Summe aller Messstände, A6)")
# Interpretation: Summe der beobachteten Füllstände zwischen Leerungen entspricht dem
# angelieferten Glas je (Location_id, Farbe) über den Zeitraum (A4/A5).
# Hinweis: Erstmessungen ohne Vorgänger enthalten ggf. einen Rest aus Vorperioden -> konservativ belassen (leichter Overestimate).
t1 = d.groupby("material_type").agg(messungen=("anteil", "size"), ueber=("ueber", "sum"), anteil_sum=("anteil", "sum"))
t1["behälter_m3"] = [A6[f] for f in t1.index]
t1["v_a6"] = (t1.anteil_sum * t1["behälter_m3"]).round(0)
t1["v_a6k"] = [round(sum(d.loc[d.material_type == f, "v_a6k"]), 0) for f in t1.index]
print(t1.to_string())
print(f"Alle Farben: A6 {t1.v_a6.sum():.0f} m³ | A6-kompakt {t1.v_a6k.sum():.0f} m³")
g_v1 = d.anteil.sum()
print(f"Vergleich gleichmäßige Kammer (V-1): {g_v1 * V1['klein']:.0f} – {g_v1 * V1['standard']:.0f} – {g_v1 * V1['groß']:.0f} m³")

h("2 Volumen je Leerung (Besuch) — nur gemessene Kammern, A6")
# Ein Besuch misst eine Teilmenge der Kammern und leert alle (A1). Das Volumen der
# ungemessenen Kammern ist nicht beobachtet -> hier nur der gemessene Teil (Untergrenze).
v = d.groupby(["Location_id", "date"]).agg(v_a6=("v_a6", "sum"), farben=("material_type", "nunique")).reset_index()
print("Besuche:", len(v), "| Ø gemessene Kammern je Besuch:", round(v.farben.mean(), 2))
print(f"  Volumen je Besuch (A6, nur gemessene): Median {v.v_a6.median():.2f} m³ | Mittel {v.v_a6.mean():.2f} | P90 {v.v_a6.quantile(.9):.2f}")
print("Achtung: Untergrenze, ungemessene Kammern fehlen (A1 sagt nur 'geleert', nicht 'wie voll').")

h("3 Volumen je Standort über den Zeitraum (A6)")
t3 = d.groupby("Location_id").v_a6.sum().round(1)
print("Standorte:", len(t3), "| Summe:", round(t3.sum(), 1), "m³ | Median je Standort:", round(t3.median(), 1),
      "| P10:", round(t3.quantile(.1), 1), "| P90:", round(t3.quantile(.9), 1))

h("4 Mindestvolumen hinter overfull (Untergrenze, A3/V-2)")
t4 = d[d.ueber].groupby("material_type").size().rename("n_overfull").to_frame()
t4["min_m3"] = (t4.n_overfull * [A6[f] for f in t4.index]).round(0)
print(t4.to_string())
print(f"Über 100%-Marke hinaus mindestens: A6 {t4.min_m3.sum():.0f} m³ | exakter Wert unbekannt")

h("5 Was diese Zahlen NICHT sind")
print("- Kein Gewicht (dafür wäre Materialdichte nötig, externe Variable, nicht recherchiert)")
print("- Keine exakte Mengenwahrheit: Ergebnis von A6 ('modelliert'), Annahme für alle 449 Standorte; Zielzahl bleibt 'eingesparte Leerungen %' (AGENTS.md §5)")
