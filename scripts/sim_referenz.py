#!/usr/bin/env python3
"""Referenz-Implementierung der Simulation aus docs/KINO_VERTRAG.md.

Unabhaengig von sim/kino.html gebaut: dieselbe Spezifikation, zwei Implementierungen.
Dient als Gegenprobe fuer die HTML-Seite.

Aufruf:
  python scripts/sim_referenz.py --s 5 --m 1 --strategie ist --schwelle 80
  python scripts/sim_referenz.py --json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
JSON_DATEI = ROOT / "data" / "derived" / "orte.json"

PERIODE_OHNE_GAP = 348.0   # Ort mit nur einem Besuch: einmal im Fenster
WARMLAUF = 90              # Tage ohne Zaehlung
TAGE = 348                 # Messfenster
VOLL = 100.0               # >= 100 % gilt als voll/uebervoll (Daten: zensiertes 'overfull')

# Ist-Durchsatz und Ausgangsabstand kommen aus data/derived/orte.json (meta),
# nicht aus fest verdrahteten Zahlen. Ohne Daten: die dokumentierten Ausgangswerte.
K0_DEFAULT = 12.8          # Stopps/Tag im Ist-Durchsatz (4.468 Besuche / 348 Tage)
S0_DEFAULT = 5.0           # Abstandseinheiten zwischen benachbarten Orten im Ist-Fall


def lade() -> dict:
    d = json.loads(JSON_DATEI.read_text(encoding="utf-8"))
    orte = d["orte"]
    n = len(orte)
    maxc = max(len(o["container"]) for o in orte)
    rate = np.zeros((n, maxc), dtype=float)
    for i, o in enumerate(orte):
        for j, c in enumerate(o["container"]):
            rate[i, j] = c["rate"] if c["rate"] is not None else 0.0
    gap = np.array([o["gap"] if o["gap"] is not None else np.nan for o in orte], dtype=float)

    # Kalibrierung: der Ist-Rhythmus soll genau die beobachteten Besuche verlangen
    meta = d["meta"]
    besuche_pro_tag = meta["besuche"] / meta["tage"]
    mit_gap = ~np.isnan(gap)
    faktor = float(meta.get("kalibrierungsfaktor")
                   or (1.0 / gap[mit_gap]).sum() / besuche_pro_tag)
    periode = np.where(mit_gap, gap * faktor, PERIODE_OHNE_GAP)

    return {"ids": [o["id"] for o in orte], "rate": rate, "gap": gap, "periode": periode,
            "faktor": faktor, "besuche_pro_tag": besuche_pro_tag,
            "k0": float(meta.get("k0_pro_tag", K0_DEFAULT)),
            "s0": float(meta.get("s0", S0_DEFAULT)),
            "anzahl_container": [len(o["container"]) for o in orte], "meta": meta}


def run(s: float = 5.0, m: int = 1, strategie: str = "ist", schwelle: float = 80.0,
        warmlauf: int = WARMLAUF, tage: int = TAGE, daten: dict | None = None) -> dict:
    d = daten or lade()
    rate, periode, n = d["rate"], d["periode"], len(d["ids"])
    if strategie not in ("ist", "fuell"):
        raise ValueError(f"unbekannte Strategie: {strategie}")

    fill = np.zeros_like(rate)
    gueltig = np.zeros_like(rate, dtype=bool)
    for i, c in enumerate(d["anzahl_container"]):
        gueltig[i, :c] = True
    budget = 0.0
    k_ges = m * d["k0"] * d["s0"] / s
    naechste = np.array([i * periode[i] / n for i in range(n)], dtype=float)

    leerungen = 0
    ueberlauf_tage = 0
    voll_bei_leerung = 0
    ueber_100_bei_leerung = 0
    max_summe = 0.0
    faellig_summe = 0
    fuell_summe = 0.0
    fuell_zaehler = 0
    abgeholt_summe = 0.0
    tage_verlauf = []

    # Producer-Groesse: Summe aller Kammer-Raten (%/Tag), abgeleitet aus der CSV.
    rate_summe = float(rate[gueltig].sum())

    for tag in range(warmlauf + tage):
        fill += rate
        maxfill = fill.max(axis=1)
        messfenster = tag >= warmlauf

        if strategie == "ist":
            faellig = np.where(tag >= naechste)[0]
        else:
            faellig = np.where(maxfill >= schwelle)[0]

        if messfenster:
            ueberlauf_tage += int((maxfill >= VOLL).sum())
            zensiert = fill[gueltig & (fill <= VOLL)]
            fuell_summe += float(zensiert.sum())
            fuell_zaehler += int(zensiert.size)
            faellig_summe += int(faellig.size)

        budget += k_ges
        bedient = 0
        if faellig.size:
            ordnung = sorted(faellig.tolist(), key=lambda i: (-maxfill[i], d["ids"][i]))
            for i in ordnung:
                if budget < 1.0:
                    break
                budget -= 1.0
                bedient += 1
                if messfenster:
                    # Consumer-Groesse: der Stand, der bei der Leerung abgeholt wird.
                    # overfull ist zensiert und wird wie in der CSV als 100 gezaehlt.
                    abgeholt_summe += float(np.minimum(fill[i], VOLL).sum())
                fill[i, :] = 0.0
                if strategie == "ist":
                    naechste[i] = tag + periode[i]
                if messfenster:
                    leerungen += 1
                    max_summe += min(VOLL, float(maxfill[i]))
                    if maxfill[i] >= VOLL:
                        voll_bei_leerung += 1
                    if maxfill[i] > VOLL:
                        ueber_100_bei_leerung += 1

        if messfenster:
            # Je Tag zusaetzlich Bedarf und Abdeckung: das Kino bewertet damit den Tag
            # (Kalender), keine Kennzahl haengt daran.
            ueberlauf_heute = int((maxfill >= VOLL).sum())
            tage_verlauf.append({"tag": tag - warmlauf + 1,
                                 "ueberlauf_tage": ueberlauf_heute,
                                 "leerungen": leerungen,
                                 "faellig": int(faellig.size),
                                 "bedient": bedient,
                                 "ueberlauf_heute": ueberlauf_heute})

    return {
        "parameter": {"s": s, "m": m, "strategie": strategie, "schwelle": schwelle,
                      "warmlauf": warmlauf, "tage": tage},
        "tag": tage,
        "leerungen": leerungen,
        "ueberlauf_tage": ueberlauf_tage,
        "voll_bei_leerung_pct": round(100 * voll_bei_leerung / leerungen, 2) if leerungen else 0.0,
        "ueber_100_bei_leerung_pct": round(100 * ueber_100_bei_leerung / leerungen, 2) if leerungen else 0.0,
        "ueberlauf_quote_pct": round(100 * ueberlauf_tage / (n * tage), 2),
        "mittel_max_bei_leerung_pct": round(max_summe / leerungen, 2) if leerungen else 0.0,
        "fuell_mittel": round(fuell_summe / fuell_zaehler, 2) if fuell_zaehler else 0.0,
        "wegeinheiten": round(s * leerungen, 2),
        "auslastung_pct": round(100 * leerungen / faellig_summe, 2) if faellig_summe else 0.0,
        "stopps_pro_tag": round(leerungen / tage, 3),
        "faellig_summe": faellig_summe,
        "soll_stopps_pro_tag": round(k_ges, 3),
        "kalibrierungsfaktor": round(d["faktor"], 4),
        # Producer/Consumer in Prozentpunkten (Pp): produziert = Summe der Kammer-Raten
        # x Messtage, abgeholt = Summe der Staende bei der Leerung.
        "produziert_pp_pro_tag": round(rate_summe, 2),
        "abgeholt_pp_pro_tag": round(abgeholt_summe / tage, 2),
        "produziert_pp": round(rate_summe * tage, 1),
        "abgeholt_pp": round(abgeholt_summe, 1),
        "bilanz_pp": round(rate_summe * tage - abgeholt_summe, 1),
        "tagesverlauf": tage_verlauf,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--s", type=float, default=5.0)
    ap.add_argument("--m", type=int, default=1)
    ap.add_argument("--strategie", choices=["ist", "fuell"], default="ist")
    ap.add_argument("--schwelle", type=float, default=80.0)
    ap.add_argument("--json", action="store_true", help="Ausgabe als JSON")
    ap.add_argument("--ohne-verlauf", action="store_true", help="Tagesverlauf weglassen")
    args = ap.parse_args()

    daten = lade()
    res = run(args.s, args.m, args.strategie, args.schwelle, daten=daten)
    d = daten
    if args.ohne_verlauf:
        res.pop("tagesverlauf")
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    print(f"Parameter: s={args.s}  Autos={args.m}  Strategie={args.strategie}"
          + (f"  Schwelle={args.schwelle}" if args.strategie == "fuell" else ""))
    print(f"Kalibrierung Ist-Rhythmus: Faktor {res['kalibrierungsfaktor']}")
    print(f"Leerungen:              {res['leerungen']}")
    print(f"Stopps/Tag (Ist/Soll):   {res['stopps_pro_tag']} / {res['soll_stopps_pro_tag']}")
    print(f"Ueberlauf-Tage:          {res['ueberlauf_tage']} ({res['ueberlauf_quote_pct']} % der Ort-Tage)")
    print(f"Voll/uebervoll b. Leerung: {res['voll_bei_leerung_pct']} %  (Daten: "
          f"{d['meta']['daten_voll_bei_leerung_pct']} %)")
    print(f"davon > 100 %:           {res['ueber_100_bei_leerung_pct']} %  (Daten overfull: "
          f"{d['meta']['daten_overfull_bei_leerung_pct']} %)")
    print(f"Mittel hoechste Kammer: {res['mittel_max_bei_leerung_pct']} %  (Daten: "
          f"{d['meta']['daten_mittel_max_bei_leerung_pct']} %)")
    print(f"Mittel-Fuellstand:      {res['fuell_mittel']} %")
    print(f"Wegeinheiten:           {res['wegeinheiten']}")
    print(f"Auslastung:             {res['auslastung_pct']} %")


if __name__ == "__main__":
    main()
