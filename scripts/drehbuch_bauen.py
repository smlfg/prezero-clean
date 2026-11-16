#!/usr/bin/env python3
"""Baut die Drehbuch-Dateien (Szenarien) aus dem LKW-Katalog.

Aufruf: python scripts/drehbuch_bauen.py
Ausgabe: data/derived/drehbuch/*.json

Keine Zahl steht von Hand in einer Drehbuch-Datei: Ladevolumen und Bezeichnungen
kommen aus scripts/lkw_katalog.py (recherchiert, V-5). Die Simulationsparameter
stehen hier als Szenario-Definition — sie sind Modellgroessen (Herkunft S/A).

Das LKW ist ein PLATZHALTER: es aendert den Lauf nicht. Das Schema verbietet zusaetzliche
Parameterfelder, damit ein Etikett nicht versehentlich ins Modell einspeist.
"""
from __future__ import annotations

import json
from pathlib import Path

from lkw_katalog import LKW, PLATZHALTER_TEXT, nach_id

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived" / "drehbuch"
SCHEMA_DATEI = ROOT / "data" / "derived" / "drehbuch.schema.json"

# Simulationsparameter je Szenario. Standard = der beobachtete Ist-Zustand.
#   abstand  = 5,0 Abstandseinheiten (S0, gesetzt)
#   autos    = 1 LKW (S)
#   strategie= "ist"  (A: aus dem beobachteten Rhythmus kalibriert)
#   schwelle = 80 %  (S, nur wirksam bei Strategie "fuell")
SZENARIEN = [
    {
        "datei": "ist-zustand",
        "name": "Ist-Zustand",
        "beschreibung": "Beobachteter Rhythmus, ein LKW, Standardcontainer.",
        "parameter": {"abstand": 5.0, "autos": 1, "strategie": "ist", "schwelle": 80},
        "lkw_id": "gc23",
    },
    {
        "datei": "gc23",
        "name": "Glas-Sammelfahrzeug GC 23",
        "beschreibung": "Ist-Rhythmus mit dem Glas-Sammelfahrzeug als Etikett.",
        "parameter": {"abstand": 5.0, "autos": 1, "strategie": "ist", "schwelle": 80},
        "lkw_id": "gc23",
    },
    {
        "datei": "hecklader-x4h",
        "name": "Hecklader MEDIUM X4H",
        "beschreibung": "Ist-Rhythmus, LKW-Anzahl 2, Hecklader als Etikett.",
        "parameter": {"abstand": 5.0, "autos": 2, "strategie": "ist", "schwelle": 80},
        "lkw_id": "x4h",
    },
    {
        "datei": "hakenlift",
        "name": "Hakenlift Eurolift HL",
        "beschreibung": "Leerung nach Füllstand (Schwelle 70 %), Hakenlift als Etikett.",
        "parameter": {"abstand": 5.0, "autos": 2, "strategie": "fuell", "schwelle": 70},
        "lkw_id": "hakenlift",
    },
]

HERKUNFT = {
    "abstand": "S",
    "autos": "S",
    "strategie": "A",
    "schwelle": "S",
    "lkw": "R",
}


def baue(sz: dict) -> dict:
    obj = nach_id(sz["lkw_id"])
    return {
        "$schema": "../drehbuch.schema.json",
        "name": sz["name"],
        "beschreibung": sz["beschreibung"],
        "parameter": sz["parameter"],
        "lkw": {
            "id": obj["id"],
            "name": obj["name"],
            "volumen_m3": obj["volumen_m3"],
            "vorschau_bild": f"bilder/lkw/{obj['id']}.png",
            "wirkung": PLATZHALTER_TEXT,
            "quelle": obj["quelle"],
        },
        "herkunft": dict(HERKUNFT),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for sz in SZENARIEN:
        d = baue(sz)
        ziel = OUT / f"{sz['datei']}.json"
        with ziel.open("w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"geschrieben: {ziel.relative_to(ROOT)}  ({d['name']})")

    print()
    print(f"Schema: {SCHEMA_DATEI.relative_to(ROOT)}")
    print(f"Drehbuch-Dateien: {len(SZENARIEN)}")
    print("Hinweis: das LKW ist ein Platzhalter — es aendert den Lauf nicht.")


if __name__ == "__main__":
    main()
