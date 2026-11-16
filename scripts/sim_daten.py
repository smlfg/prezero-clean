#!/usr/bin/env python3
"""Baut die Datenschnittstelle fuer das Simulations-Kino aus der Original-CSV.

Ausgabe: data/derived/orte.json, Schema siehe docs/KINO_VERTRAG.md Abschnitt 4.

Es wird nichts geschaetzt und nichts von Hand eingetragen. Alle Zahlen kommen aus
den vier CSV-Spalten (Location_id, material_type, date, fill_level_perc) nach den
Konventionen von scripts/fakten.py:

- rate (%/Tag je Location_id+material_type): Median aus p / tage ueber numerische
  Folgemessungen desselben Containers, nur p > 0 und tage > 0. `overfull` ist Text
  und damit zensiert, es geht nicht in die Rate ein (Annahmen A2 + A4).
- n: Anzahl Messungen dieses Containers in der CSV (alle, auch 0 und `overfull`).
- gap (Tage): Median der Abstaende aufeinanderfolgender Besuche des Ortes
  (Besuch = Location_id + date), null bei nur einem Besuch.
- Container ohne verwertbare Rate bekommen rate = null und werden in
  meta.container_ohne_rate gezaehlt.
- drehbuch: die Szenario-Dateien aus data/derived/drehbuch/*.json werden eingebettet,
  damit das Kino sie ohne Server laden kann. Das LKW darin ist ein PLATZHALTER
  (recherchiert, wirkt nicht auf den Lauf).

Aufruf: .venv/bin/python scripts/sim_daten.py [pfad_zur_csv]
"""
import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "raw" / "glass_fill_levels_anonymized_f.csv"
OUT = ROOT / "data" / "derived" / "orte.json"
DREHBUCH_DIR = ROOT / "data" / "derived" / "drehbuch"
S0 = 5.0
WARMLAUF = 90  # Tage ohne Zaehlung, gesetzt (siehe docs/KINO_VERTRAG.md)

SPALTEN = ["Location_id", "material_type", "date", "fill_level_perc"]

# Herkunftsmarkierung fuer das Kino. Vier Kategorien, mehr nicht.
#   M = gemessen   -> steht so in der CSV
#   A = abgeleitet -> aus Messwerten berechnet, keine Annahme
#   S = gesetzt    -> Annahme, Modellgroesse, Startwert, Darstellung
#   R = recherchiert -> externe Quelle mit Wert und Abrufdatum, wirkt nicht auf den Lauf
KATEGORIEN = {
    "M": {
        "code": "M",
        "kurz": "gemessen",
        "lang": "Direkt aus der CSV gemessen.",
    },
    "A": {
        "code": "A",
        "kurz": "abgeleitet",
        "lang": "Aus den Messwerten berechnet. Keine Annahme, aber keine Messung.",
    },
    "S": {
        "code": "S",
        "kurz": "gesetzt",
        "lang": "Von uns gesetzt: Annahme, Modellgröße, Startwert oder Darstellung.",
    },
    "R": {
        "code": "R",
        "kurz": "recherchiert",
        "lang": "Aus einer externen Quelle mit Abrufdatum. Wirkt nicht auf die Simulation.",
    },
}

# Welche Groesse des meta-Blocks welche Herkunft hat. Eine Liste, ein Ort:
# das Kino liest sie und setzt die Marker - nichts wird im HTML von Hand markiert.
HERKUNFT_META = {
    "messungen": "M",
    "orte": "M",
    "container": "M",
    "besuche": "M",
    "tage": "M",
    "daten_besuche": "M",
    "daten_voll_bei_leerung_pct": "M",
    "daten_overfull_bei_leerung_pct": "M",
    "daten_mittel_max_bei_leerung_pct": "M",
    "daten_ueberlauf_messungen_pct": "M",
    "k0_pro_tag": "A",
    "kalibrierungsfaktor": "A",
    "s0": "S",
}

# Herkunft der Groessen, die nicht im meta-Block stehen, aber im Kino sichtbar sind.
HERKUNFT_SONSTIGE = {
    "rate": "A",
    "gap": "A",
    "container_ohne_rate": "M",
    "warmlauf_tage": "S",
    # Kapazitaet enthaelt das gesetzte s0 und den gesetzten Abstand s —
    # Modellgroesse, nicht Ableitung aus Messwerten.
    "stopps_pro_tag_soll": "S",
    "wegeinheiten": "S",
    "auslastung_pct": "S",
    "ueberlauf_tage": "S",
    "fuell_mittel": "S",
    "ist_rhythmus": "A",
    "schwelle": "S",
    "ring_reihenfolge": "S",
    "lkw_objekt": "R",
    "lkw_volumen_m3": "R",
    "container_volumen_m3": "R",
}


def lade(csv_pfad):
    d = pd.read_csv(csv_pfad, parse_dates=["date"], usecols=SPALTEN)
    d["p"] = pd.to_numeric(d.fill_level_perc, errors="coerce")  # overfull -> NaN (zensiert)
    return d.sort_values(["Location_id", "material_type", "date"]).reset_index(drop=True)


def raten(d):
    """Median-Rate je Container aus numerischen Folgemessungen."""
    d = d.copy()
    d["tage"] = d.groupby(["Location_id", "material_type"]).date.diff().dt.days
    x = d[(d.p > 0) & (d.tage > 0)].copy()
    x["rate"] = x.p / x.tage
    med = x.groupby(["Location_id", "material_type"]).rate.median()
    n = d.groupby(["Location_id", "material_type"]).size()
    return med, n


def orts_gaps(d):
    """Median der Besuchsabstaende je Ort; NaN bei nur einem Besuch."""
    v = d[["Location_id", "date"]].drop_duplicates().sort_values(["Location_id", "date"])
    v["gap"] = v.groupby("Location_id").date.diff().dt.days
    return v.groupby("Location_id").gap.median()


def besuchs_stats(d):
    """Ist-Referenz je Besuch: hoechster Kammerstand und overfull-Flag."""
    x = d.copy()
    x["over"] = x.fill_level_perc.eq("overfull")
    x["p_cap"] = pd.to_numeric(x.fill_level_perc.where(~x["over"]), errors="coerce").fillna(100.0)
    v = x.groupby(["Location_id", "date"]).agg(max_cap=("p_cap", "max"),
                                              any_over=("over", "any")).reset_index()
    return {
        "besuche": int(len(v)),
        "voll_ge100_pct": round(100 * float((v.max_cap >= 100).mean()), 2),
        "overfull_pct": round(100 * float(v.any_over.mean()), 2),
        "mittel_max_pct": round(float(v.max_cap.mean()), 2),
        "ueberfull_messungen_pct": round(100 * float(x["over"].mean()), 2),
    }


def kalibrierungsfaktor(gaps, besuche, tage):
    """Faktor, damit der Ist-Rhythmus genau die beobachteten Besuche verlangt."""
    g = gaps.dropna()
    if len(g) == 0:
        return 1.0
    return round(float((1.0 / g).sum()) / (besuche / tage), 4)


def lade_drehbuch() -> list:
    """Die Szenario-Dateien einlesen und einbetten.

    Das LKW je Szenario ist ein PLATZHALTER: recherchiert (V-5), ohne Wirkung auf
    den Lauf. Der Vorschau-Bildpfad bleibt RELATIV zum Repo-Wurzelverzeichnis.
    Die Seite (sim/kino.html) rechnet ihn selbst um - so funktioniert der Pfad
    per Doppelklick (file://) genauso wie ueber einen HTTP-Server.
    """
    szenarien = []
    if not DREHBUCH_DIR.exists():
        return szenarien
    for p in sorted(DREHBUCH_DIR.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        d["datei"] = p.name
        szenarien.append(d)
    return szenarien


def baue(d):
    med, n_messungen = raten(d)
    gaps = orts_gaps(d)
    drehbuch = lade_drehbuch()

    orte = []
    for lid in sorted(d.Location_id.unique()):
        container = []
        for farbe in sorted(d.loc[d.Location_id == lid, "material_type"].unique()):
            r = med.get((lid, farbe))
            container.append({
                "farbe": farbe,
                "rate": None if pd.isna(r) else round(float(r), 4),
                "n": int(n_messungen[(lid, farbe)]),
            })
        g = gaps.get(lid)
        orte.append({
            "id": lid,
            "gap": None if pd.isna(g) else round(float(g), 2),
            "container": container,
        })

    tage = int((d.date.max() - d.date.min()).days)
    besuche = int(d[["Location_id", "date"]].drop_duplicates().shape[0])
    b = besuchs_stats(d)
    meta = {
        "erzeugt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "quelle": "data/raw/glass_fill_levels_anonymized_f.csv",
        "skript": "scripts/sim_daten.py",
        "orte": len(orte),
        "container": int(d.groupby(["Location_id", "material_type"]).ngroups),
        "messungen": int(len(d)),
        "besuche": besuche,
        "tage": tage,
        "k0_pro_tag": round(besuche / tage, 1),
        "s0": S0,
        "container_ohne_rate": int(sum(1 for o in orte for c in o["container"] if c["rate"] is None)),
        # Ist-Referenz aus den Daten: Anteil der Besuche, bei denen mindestens eine
        # Kammer voll (>= 100 %) bzw. ausdruecklich 'overfull' war.
        "daten_besuche": b["besuche"],
        "daten_voll_bei_leerung_pct": b["voll_ge100_pct"],
        "daten_overfull_bei_leerung_pct": b["overfull_pct"],
        "daten_mittel_max_bei_leerung_pct": b["mittel_max_pct"],
        "daten_ueberlauf_messungen_pct": b["ueberfull_messungen_pct"],
        # Kalibrierung: der Ist-Rhythmus soll genau die beobachteten Besuche verlangen
        "kalibrierungsfaktor": kalibrierungsfaktor(gaps, besuche, tage),
        "warmlauf_tage": WARMLAUF,
        # Herkunftsmarkierung: welche Groesse ist gemessen, abgeleitet oder gesetzt.
        # Das Kino liest diese Tags und setzt die Marker - keine Handarbeit im HTML.
        "herkunft": {
            "kategorien": KATEGORIEN,
            "meta": HERKUNFT_META,
            "sonstige": HERKUNFT_SONSTIGE,
        },
        # Drehbuch-Szenarien (Platzhalter-LKW, recherchiert, ohne Wirkung auf den Lauf)
        "drehbuch_anzahl": len(drehbuch),
    }
    return {"meta": meta, "orte": orte, "drehbuch": drehbuch}


def main():
    d = lade(CSV)
    daten = baue(d)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=1)
        f.write("\n")

    meta = daten["meta"]
    raten_liste = pd.Series([c["rate"] for o in daten["orte"] for c in o["container"] if c["rate"] is not None])
    ohne_gap = sum(1 for o in daten["orte"] if o["gap"] is None)
    groesse = OUT.stat().st_size

    print(f"orte: {meta['orte']}")
    print(f"container: {meta['container']}")
    print(f"container_ohne_rate: {meta['container_ohne_rate']}")
    print("rate %/Tag (n={}): P10 {:.3f} | Median {:.3f} | P90 {:.3f}".format(
        len(raten_liste),
        raten_liste.quantile(0.1),
        raten_liste.median(),
        raten_liste.quantile(0.9),
    ))
    print(f"orte_ohne_gap (nur ein Besuch): {ohne_gap}")
    print(f"drehbuch: {meta['drehbuch_anzahl']} Szenarien eingebettet (LKW = Platzhalter)")
    print(f"geschrieben: {OUT.relative_to(ROOT)} ({groesse} Bytes)")


if __name__ == "__main__":
    main()
