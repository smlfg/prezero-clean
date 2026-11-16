# prezero-clean

Sauberer Neustart: PreZero Glascontainer, nur mit den gegebenen Daten.

## Datenbasis

`data/raw/glass_fill_levels_anonymized_f.csv` — 11.701 Messungen, 449 Container,
17.10.2025 bis 30.09.2026. Nur diese vier Spalten: `Location_id`, `material_type`,
`date`, `fill_level_perc`.

Keine Koordinaten, keine Distanzen, keine Kosten, keine synthetischen Daten.

## Modell

- `src/domaene.py` — Domänenmodell `Glas` – `Container` – `LKW` (AGENTS.md §2).
  Container (`Location_id`) mit 1–3 Kammern je Farbe; der LKW **misst** eine
  Teilmenge der Kammern und **leert** alle. Gate: `tests/test_domaene.py`.
- `src/modell.py` — Puffer-Modell je Kammer, Füllrate je `Location_id`+`material_type`.
  Gate: `tests/test_bilanz.py` (AGENTS.md §4).

```bash
python -m pytest tests/ -q
```

## Fakten

Alle Zahlen stammen aus `scripts/fakten.py`:

```bash
python scripts/fakten.py
```

## Volumen

Sensitivity aus internen Füllständen × externer Kammervolumen-Bandbreite
(Quelle/Unsicherheit: `docs/externe_parameter.md`):

```bash
python scripts/volumen_sensitivity.py
```

## Bilder

Vier Diagnose-Bilder aus denselben Daten, ohne Modell und ohne Annahme außer A1/A2:

```bash
python scripts/bilder.py
```

`bilder/01_mechanismus.png` · `02_alle_orte.png` · `03_einheit.png` · `04_takt.png`.
Was jedes Bild zeigt und was fehlt: `bilder/LIESMICH.md`. Regeln für weitere Bilder: `assets/ui/UI_REGELN.md`.

## Regeln

Siehe `AGENTS.md` (Datenquelle, Annahmen, Bilanztest-Gate, Zielzahl), `SCOPE.md` und `assets/ui/UI_REGELN.md`.