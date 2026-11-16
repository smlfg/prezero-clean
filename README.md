# prezero-clean

Sauberer Neustart der Analyse der Glascontainer-Fuellstandsdaten
(PreZero-Challenge, Future City Hackathon Heilbronn 2026).

## Datenbasis

- `data/raw/glass_fill_levels_anonymized_f.csv` — 11.701 Messungen, 449 Locations, 1.192 `overfull`.
- `data/external/locations.csv` — Zuordnung Location_id -> lat/lon (Quelle/Konfidenz je Zeile).

Kopie der Originaldaten, keine generierten Outputs.

## Scope

Nur Daten laden, analysieren, visualisieren. Kein Routing, keine Scoring-Modelle, kein Dashboard.

## Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```