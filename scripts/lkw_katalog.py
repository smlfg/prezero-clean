#!/usr/bin/env python3
"""LKW-Objekt-Katalog — die eine Quelle fuer Etikett, Vorschau-Bild und Drehbuch.

Alle Werte sind recherchiert (Herstellerangaben), NICHT gemessen und NICHT modelliert.
Sie wirken NICHT auf die Simulation: das LKW ist ein Platzhalter-Etikett im Drehbuch.
Quelle, Unsicherheit und Abrufdatum: docs/externe_parameter.md Abschnitt V-5.
Upstream-Evidenz: docs/UPSTREAM_SEARCH.md (Abschnitt C).

Der Platzhalter-Text steht bewusst an EINER Stelle hier, damit Script, Bilder und
Drehbuch-Dateien nicht auseinanderlaufen koennen.

Aufruf: python scripts/lkw_katalog.py
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ABRUF = "2026-11-16"

# Beobachtete Ladung je Besuch (obere Schranke: alle Farben, 'overfull' = voll).
# Aus data/raw/glass_fill_levels_anonymized_f.csv, 4.468 Besuche, + A6/V-3.
# scripts/drehbuch_pruefen.py rechnet das nach; hier steht nur der Wert fuer die Beschriftung.
LADUNG_MEDIAN_M3 = 4.35

# Volumen eines PreZero-Standorts bei 100 %: weiss 3,2 + gruen 2,1 + braun 1,1 (A6/V-3).
STANDORT_VOLL_M3 = 6.4

PLATZHALTER_TEXT = "Platzhalter — noch keine Wirkung auf die Simulation"

LKW = [
    {
        "id": "gc23",
        "name": "Glas-Sammelfahrzeug GC 23",
        "hersteller": "Stummer",
        "volumen_m3": 23.0,
        "volumen_text": "23 m³",
        "typ": "Glas-Sammelfahrzeug",
        "quelle": "Stummer Fact Sheet Glass Collector GC 23 (PDF)",
        "quelle_url": "https://stummer.net/wp-content/uploads/2026/03/260330_STU_Fact_Sheet_Glassammpler_A4_ENGL.pdf",
        "beschreibung": "2-Kammer-Schneckenförderer, MGB 80–240 l, 26 t",
        # Silhouette: Laenge/Breite/Hoehe in m (Naeherung fuer die maßstaebliche Skizze)
        "laenge_m": 10.0,
        "breite_m": 2.55,
        "hoehe_m": 3.6,
        "aufbau_ab_m": 2.6,
    },
    {
        "id": "x4h",
        "name": "Hecklader MEDIUM X4H",
        "hersteller": "Zoeller",
        "volumen_m3": 29.0,
        "volumen_text": "14–29 m³",
        "typ": "Hecklader",
        "quelle": "Zoeller Datenblatt MEDIUM X4/X4H (PDF)",
        "quelle_url": "https://www.zoeller-kipper.de/wp-content/uploads/2024/02/2022.06.07_MEDIUM-X4H.pdf",
        "beschreibung": "Hecklader, 14–29 m³ Nutzvolumen, Ladeförderer 6,2 m³/min",
        "laenge_m": 8.5,
        "breite_m": 2.55,
        "hoehe_m": 3.6,
        "aufbau_ab_m": 1.8,
    },
    {
        "id": "hakenlift",
        "name": "Hakenlift Eurolift HL",
        "hersteller": "Stummer",
        "volumen_m3": 31.0,
        "volumen_text": "18–31 m³",
        "typ": "Hakenlift",
        "quelle": "Stummer Produktseite Eurolift Hooklift",
        "quelle_url": "https://stummer.net/en/products/",
        "beschreibung": "Hooklift 18–31 m³, Hebekraft 8–30 t, 2–4 Achsen",
        "laenge_m": 9.0,
        "breite_m": 2.55,
        "hoehe_m": 3.8,
        "aufbau_ab_m": 1.4,
    },
    {
        "id": "presse20",
        "name": "Presse 20 m³",
        "hersteller": "REMONDIS",
        "volumen_m3": 20.0,
        "volumen_text": "20 m³",
        "typ": "Presscontainer",
        "quelle": "REMONDIS Sammelsysteme für die Kreislaufwirtschaft (PDF)",
        "quelle_url": "https://machulez-logistik.de/wp-content/uploads/2022/07/Remondis-Sammelsysteme-fuer-die-Kreislaufwirtschaft.pdf",
        "beschreibung": "Presscontainer mit integrierter Presse",
        "laenge_m": 6.0,
        "breite_m": 2.3,
        "hoehe_m": 2.3,
        "aufbau_ab_m": 0.5,
    },
    {
        "id": "arkm36",
        "name": "Abrollkipper ARKM 36",
        "hersteller": "REMONDIS",
        "volumen_m3": 36.0,
        "volumen_text": "36 m³",
        "typ": "Abrollkipper",
        "quelle": "REMONDIS Sammelsysteme für die Kreislaufwirtschaft (PDF)",
        "quelle_url": "https://machulez-logistik.de/wp-content/uploads/2022/07/Remondis-Sammelsysteme-fuer-die-Kreislaufwirtschaft.pdf",
        "beschreibung": "Abrollkipper-Mulde, Reihe ARKM 11–48,5 m³",
        "laenge_m": 6.9,
        "breite_m": 2.55,
        "hoehe_m": 3.3,
        "aufbau_ab_m": 1.0,
    },
]


def nach_id(lkw_id: str) -> dict:
    """Ein Objekt nach seiner id. Wirft KeyError bei unbekannter id."""
    for o in LKW:
        if o["id"] == lkw_id:
            return o
    raise KeyError(f"unbekanntes LKW-Objekt: {lkw_id}")


def orte_je_tour(volumen_m3: float) -> float:
    """Reine Rechnung: wie viele Standorte passen bei der beobachteten Median-Ladung."""
    return volumen_m3 / LADUNG_MEDIAN_M3


def main() -> None:
    print(f"LKW-Objekte (recherchiert, Abrufdatum {ABRUF}) — Platzhalter, ohne Wirkung auf die Simulation")
    print(f"Referenz: {STANDORT_VOLL_M3} m³ = 1 voller PreZero-Standort (A6/V-3)")
    print(f"           {LADUNG_MEDIAN_M3} m³ = beobachtete Ladung je Besuch (Median, obere Schranke)")
    print()
    print(f"{'Objekt':<32}{'Ladevolumen':>14}{'Orte/Tour':>12}")
    print("-" * 58)
    for o in LKW:
        print(f"{o['name']:<32}{o['volumen_text']:>14}{orte_je_tour(o['volumen_m3']):>12.1f}")
    print()
    print("Quelle je Objekt: docs/externe_parameter.md V-5")


if __name__ == "__main__":
    main()
