#!/usr/bin/env python3
"""Vergleicht die JavaScript-Engine (sim/engine.js) mit der Python-Referenz.

Zwei unabhaengige Implementierungen derselben Spezifikation (docs/KINO_VERTRAG.md).
Tolleranzen laut Vertrag: +-1 Stopp, +-0,5 Pp, +-0,3 % bei Mittelwerten.

Aufruf: python scripts/sim_vergleich.py
Exitcode 0 = alles innerhalb der Toleranz, 1 = Abweichung.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sim_referenz import run  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

LAEUFE = [
    {"name": "default", "s": 5, "m": 1, "strategie": "ist", "schwelle": 80},
    {"name": "s10", "s": 10, "m": 1, "strategie": "ist", "schwelle": 80},
    {"name": "s20", "s": 20, "m": 1, "strategie": "ist", "schwelle": 80},
    {"name": "m4_ist", "s": 5, "m": 4, "strategie": "ist", "schwelle": 80},
    {"name": "m4_fuell", "s": 5, "m": 4, "strategie": "fuell", "schwelle": 80},
]

TOLERANZ = {
    "leerungen": 1,
    "ueberlauf_tage": 2,
    "voll_bei_leerung_pct": 0.5,
    "ueber_100_bei_leerung_pct": 0.5,
    "mittel_max_bei_leerung_pct": 0.3,
    "fuell_mittel": 0.3,
    "auslastung_pct": 0.5,
    "stopps_pro_tag": 0.05,
    "wegeinheiten": 2.0,
}


def js_laeufe() -> dict:
    res = subprocess.run(["node", str(ROOT / "scripts" / "sim_check.js"), "--json"],
                         capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def main() -> None:
    js = js_laeufe()
    fehler = []
    print(f"{'Lauf':<10} {'Größe':<26} {'Python':>12} {'JavaScript':>12} {'Diff':>10}")
    print("-" * 74)
    for l in LAEUFE:
        py = run(l["s"], l["m"], l["strategie"], l["schwelle"])
        for groesse, tol in TOLERANZ.items():
            a, b = float(py[groesse]), float(js[l["name"]][groesse])
            diff = abs(a - b)
            if diff > tol:
                fehler.append(f"{l['name']}/{groesse}: Python {a} vs JS {b} (Diff {diff:.3f} > Toleranz {tol})")
        a, b = py["leerungen"], js[l["name"]]["leerungen"]
        print(f"{l['name']:<10} {'Leerungen':<26} {a:>12} {b:>12} {b - a:>10}")
        a, b = py["voll_bei_leerung_pct"], js[l["name"]]["voll_bei_leerung_pct"]
        print(f"{'':<10} {'voll/übervoll b. Leerung %':<26} {a:>12} {b:>12} {b - a:>10.3f}")
        a, b = py["ueber_100_bei_leerung_pct"], js[l["name"]]["ueber_100_bei_leerung_pct"]
        print(f"{'':<10} {'davon > 100 %':<26} {a:>12} {b:>12} {b - a:>10.3f}")
        a, b = py["fuell_mittel"], js[l["name"]]["fuell_mittel"]
        print(f"{'':<10} {'Ø Füllstand %':<26} {a:>12} {b:>12} {b - a:>10.3f}")
        a, b = py["ueberlauf_tage"], js[l["name"]]["ueberlauf_tage"]
        print(f"{'':<10} {'Überlauf-Tage':<26} {a:>12} {b:>12} {b - a:>10}")
        print()

    if fehler:
        print("ABWEICHUNGEN ausserhalb der Toleranz:")
        for f in fehler:
            print("  -", f)
        sys.exit(1)
    print("Alle Läufe innerhalb der Toleranz.")


if __name__ == "__main__":
    main()
