# prezero-clean

Sauberer Neustart: PreZero Glascontainer, nur mit den gegebenen Daten.

## Datenbasis

`data/raw/glass_fill_levels_anonymized_f.csv` — 11.701 Messungen, 449 Container,
17.10.2025 bis 30.09.2026. Nur diese vier Spalten: `Location_id`, `material_type`,
`date`, `fill_level_perc`.

Keine Koordinaten, keine Distanzen, keine Kosten, keine synthetischen Daten.

## Fakten

Alle Zahlen stammen aus `scripts/fakten.py`:

```bash
python scripts/fakten.py
```

## Regeln

Siehe `AGENTS.md` (Datenquelle, Annahmen, Bilanztest-Gate, Zielzahl) und `SCOPE.md`.