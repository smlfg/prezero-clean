#!/usr/bin/env python3
"""Berechnet alle Fakten aus der Original-CSV. Jede Zahl in README.md/AGENTS.md stammt von hier.
Aufruf: python scripts/fakten.py [pfad_zur_csv]"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

CSV = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "data" / "raw" / "glass_fill_levels_anonymized_f.csv"
d = pd.read_csv(CSV, parse_dates=["date"])
def h(t): print(f"\n== {t}")

h("1 Form")
print("Spalten:", list(d.columns), "| Typen:", dict(d.dtypes.astype(str)))
print("Zeilen:", len(d), "| fehlende Werte:", int(d.isna().sum().sum()), "| exakte Duplikate:", int(d.duplicated().sum()))
print("Zeitraum:", d.date.min().date(), "bis", d.date.max().date(), "| Tage:", (d.date.max() - d.date.min()).days)
print("Zeitstempel hat Uhrzeit:", bool((d.date != d.date.dt.normalize()).any()), "(nur Datum, keine Uhrzeit)")

h("2 Füllstand: Werte")
print(d.fill_level_perc.value_counts().sort_index().to_string())
d["ueber"] = d.fill_level_perc.eq("overfull")
d["p"] = pd.to_numeric(d.fill_level_perc.where(~d.ueber))
print("Numerisch > 100:", int((d.p > 100).sum()), "| Zeile 'overfull' (Text):", int(d.ueber.sum()), f"= {d.ueber.mean():.1%}")
print("Genau 100:", int((d.p == 100).sum()), f"= {(d.p == 100).mean():.1%}", "| Genau 0:", int((d.p == 0).sum()))
print("Stufen numerisch:", sorted(d.p.dropna().unique().astype(int).tolist()))

h("3 Container-IDs und Glasarten")
print("Container-IDs:", d.Location_id.nunique(), "| Container+Farbe:", d.groupby(["Location_id", "material_type"]).ngroups)
print("Messungen je Farbe:\n" + d.material_type.value_counts().to_string())
print("Überlauf-Anteil je Farbe:\n" + d.groupby("material_type").ueber.mean().map("{:.1%}".format).to_string())
print("Farben pro ID (Anzahl IDs):", d.groupby("Location_id").material_type.nunique().value_counts().sort_index().to_dict())
print("Doppelte (ID,Farbe,Datum):", int(d.duplicated(["Location_id", "material_type", "date"]).sum()))

h("4 Besuche (ID+Datum = ein LKW-Besuch, Annahme)")
v = d.groupby(["Location_id", "date"]).material_type.nunique().rename("farben").reset_index().sort_values(["Location_id", "date"])
print("Besuche:", len(v), "| Farben je Besuch (Anzahl Besuche):", v.farben.value_counts().sort_index().to_dict())
v["abstand"] = v.groupby("Location_id").date.diff().dt.days
print("Messungen je ID: Median", d.groupby("Location_id").size().median(), "min", d.groupby("Location_id").size().min(), "max", d.groupby("Location_id").size().max())
print("Besuche je ID: Median", v.groupby("Location_id").size().median(), "min", v.groupby("Location_id").size().min(), "max", v.groupby("Location_id").size().max())
print("Abstand zwischen Besuchen (Tage): min", v.abstand.min(), "P10", v.abstand.quantile(.1), "Median", v.abstand.median(), "P90", v.abstand.quantile(.9), "max", v.abstand.max())
print("Wochentage Messungen (0=Mo):", d.date.dt.dayofweek.value_counts().sort_index().to_dict())

h("5 Füllstand nach Abstand zum letzten Besuch (Container+Farbe)")
d = d.sort_values(["Location_id", "material_type", "date"])
d["abstand"] = d.groupby(["Location_id", "material_type"]).date.diff().dt.days
x = d.dropna(subset=["abstand"]).copy()
x["klasse"] = pd.cut(x.abstand, [0, 7, 14, 30, 60, 400], labels=["<=7", "8-14", "15-30", "31-60", ">60"])
print(x.groupby("klasse", observed=True).agg(n=("p", "size"), mittel_fuell=("p", "mean"), ueberlauf=("ueber", "mean")).round(3).to_string())
print("Erste Messung je Container+Farbe hat keinen Vorgänger:", int(d.abstand.isna().sum()))

h("6 Bilanz-Probe (Rate * Abstand = gemessener Stand?)")
ok = x[~x.ueber & (x.abstand > 0)].copy()
ok["rate"] = ok.p / ok.abstand
r = ok.groupby(["Location_id", "material_type"]).rate.median().rename("rate_med")
ok = ok.join(r, on=["Location_id", "material_type"])
ok["pred"] = (ok.rate_med * ok.abstand).clip(upper=100)
fehler = (ok.pred - ok.p).abs()
print("Zeilen für Probe:", len(ok), "| mittlerer Fehler (Prozentpunkte, in-sample):", round(fehler.mean(), 1), "| Median:", round(fehler.median(), 1))
print("Anteil Fehler <= 10 Pp:", f"{(fehler <= 10).mean():.1%}", "| <= 20 Pp:", f"{(fehler <= 20).mean():.1%}")
print("Rate %/Tag je Container+Farbe: P10", round(r.quantile(.1), 2), "Median", round(r.median(), 2), "P90", round(r.quantile(.9), 2))
print("Tage bis 100% bei Median-Rate (Median über Container+Farbe):", round((100 / r[r > 0]).median(), 1))
print("Lesehinweis: kein Schwellenwert festgelegt; der Bilanztest-Grenzwert ist offene Frage an den Stakeholder.")
