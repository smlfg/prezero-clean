#!/usr/bin/env python3
"""Prueft die Drehbuch-Dateien gegen das Schema und gegen den Katalog.

Aufruf: python scripts/drehbuch_pruefen.py
Exitcode 0 = alles in Ordnung, 1 = Fehler.

Geprueft wird dreifach:
  1. Schema: Struktur, Wertebereiche, keine zusaetzlichen Felder.
  2. Katalog: LKW-ID und Bezeichnungen muessen zu scripts/lkw_katalog.py passen.
  3. Trennung: das LKW ist ein Platzhalter. Es darf keinen Simulationsparameter
     enthalten und keine Kennzahl des Laufs beeinflussen (AGENTS.md Abschnitt 1).

Upstream: docs/UPSTREAM_SEARCH.md (jsonschema).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lkw_katalog import LKW, PLATZHALTER_TEXT, nach_id  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DREHBUCH = ROOT / "data" / "derived" / "drehbuch"
SCHEMA_DATEI = ROOT / "data" / "derived" / "drehbuch.schema.json"

# Das Schema erlaubt genau diese vier Simulationsparameter. Alles andere waere
# ein Versuch, ein Etikett ins Modell einzuschleusen.
ERLAUBTE_PARAMETER = {"abstand", "autos", "strategie", "schwelle"}


def lade_szenarien() -> list[tuple[Path, dict]]:
    out = []
    for p in sorted(DREHBUCH.glob("*.json")):
        out.append((p, json.loads(p.read_text(encoding="utf-8"))))
    return out


def pruefe_schema(daten: dict, validator) -> list[str]:
    fehler = []
    for e in sorted(validator.iter_errors(daten), key=lambda x: list(x.path)):
        pfad = "/".join(str(x) for x in e.path) or "(wurzel)"
        fehler.append(f"Schema: {pfad}: {e.message}")
    return fehler


def pruefe_katalog(daten: dict) -> list[str]:
    fehler = []
    lkw = daten.get("lkw") or {}
    lkw_id = lkw.get("id")
    try:
        obj = nach_id(lkw_id)
    except KeyError:
        return [f"Katalog: unbekanntes LKW-Objekt '{lkw_id}'"]

    if lkw.get("name") != obj["name"]:
        fehler.append(
            f"Katalog: Name '{lkw.get('name')}' weicht vom Katalog ab ({obj['name']})")
    if lkw.get("volumen_m3") != obj["volumen_m3"]:
        fehler.append(
            f"Katalog: Ladevolumen {lkw.get('volumen_m3')} weicht vom Katalog ab "
            f"({obj['volumen_m3']})")
    if lkw.get("wirkung") != PLATZHALTER_TEXT:
        fehler.append("Platzhalter: der Klartext zur Wirkung fehlt oder weicht ab")
    if lkw.get("quelle") != obj["quelle"]:
        fehler.append("Katalog: Quelle weicht vom Katalog ab")
    bild = lkw.get("vorschau_bild")
    if bild:
        if not (ROOT / bild).exists():
            fehler.append(f"Vorschau: Bild fehlt: {bild}")
    return fehler


def pruefe_trennung(daten: dict) -> list[str]:
    """Das LKW ist ein Platzhalter: es darf die Simulation nicht veraendern."""
    fehler = []
    parameter = daten.get("parameter") or {}
    extra = set(parameter) - ERLAUBTE_PARAMETER
    if extra:
        fehler.append(
            f"Trennung: unerlaubte Simulationsparameter {sorted(extra)} — "
            "das LKW darf nicht ins Modell einspeisen")
    # Das LKW darf keine eigene Parameter-Sektion fuehren.
    if "parameter" in (daten.get("lkw") or {}):
        fehler.append("Trennung: das LKW-Objekt darf keine 'parameter'-Sektion haben")
    return fehler


def main() -> None:
    schema = json.loads(SCHEMA_DATEI.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    szenarien = lade_szenarien()
    if not szenarien:
        print("Keine Drehbuch-Dateien gefunden.")
        sys.exit(1)

    alle_fehler = []
    for pfad, daten in szenarien:
        fehler = (pruefe_schema(daten, validator)
                  + pruefe_katalog(daten)
                  + pruefe_trennung(daten))
        status = "OK " if not fehler else "FEHLER"
        print(f"[{status}] {pfad.relative_to(ROOT)}  — {daten.get('name')}")
        for f in fehler:
            print(f"         {f}")
        alle_fehler.extend(fehler)

    print()
    print(f"{len(szenarien)} Drehbuch-Dateien geprueft, {len(alle_fehler)} Fehler")
    if alle_fehler:
        sys.exit(1)
    print("Alle Drehbuch-Dateien sind gueltig.")


if __name__ == "__main__":
    main()
