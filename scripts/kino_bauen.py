#!/usr/bin/env python3
"""Baut sim/kino.html aus sim/kino_vorlage.html + sim/engine.js + data/derived/orte.json.

Engine und Daten werden inline eingebettet, damit die Seite per Doppelklick (file://)
laeuft. Ein Lauf, eine Quelle: keine Zahl steht im HTML von Hand.

Aufruf: python scripts/kino_bauen.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VORLAGE = ROOT / "sim" / "kino_vorlage.html"
ENGINE = ROOT / "sim" / "engine.js"
ZIEL = ROOT / "sim" / "kino.html"
DATEN = ROOT / "data" / "derived" / "orte.json"
P_DATEN = "__DATEN__"
P_ENGINE = "/*__ENGINE__*/"


def main() -> None:
    vorlage = VORLAGE.read_text(encoding="utf-8")
    engine = ENGINE.read_text(encoding="utf-8").strip()
    daten = DATEN.read_text(encoding="utf-8").strip()

    for p in (P_DATEN, P_ENGINE):
        if p not in vorlage:
            raise SystemExit(f"Platzhalter {p} fehlt in {VORLAGE}")
    if "</script>" in daten or "</script>" in engine:
        raise SystemExit("Daten oder Engine enthalten </script> - nicht einbettbar")

    ziel_text = vorlage.replace(P_ENGINE, engine).replace(P_DATEN, daten)
    ZIEL.write_text(ziel_text, encoding="utf-8")

    meta = json.loads(daten)["meta"]
    print(f"geschrieben: {ZIEL.relative_to(ROOT)} ({ZIEL.stat().st_size / 1024:.0f} KB)")
    print(f"Daten: {meta['orte']} Orte · {meta['container']} Kammern · "
          f"{meta['messungen']} Messungen · {meta['besuche']} Besuche · "
          f"Kalibrierungsfaktor {meta['kalibrierungsfaktor']}")


if __name__ == "__main__":
    main()
