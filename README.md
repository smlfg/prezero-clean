# prezero-clean

Sauberer Neustart: Analyse und Simulation der PreZero-Glascontainer, nur mit den gegebenen Daten.

## Status

Python-Projekt mit Fakten-Skript, Domänen- und Puffer-Modell, Tests, Diagnose-Bildern und einem lokalen Simulations-Kino. Die Roh-CSV ist nicht Bestandteil des öffentlichen Repositories. Sie kann vertraulich sein und muss lokal unter `data/raw/glass_fill_levels_anonymized_f.csv` liegen (siehe `.gitignore`).

## Live-Stand

Das Simulations-Kino ist über GitHub Pages erreichbar:

<https://smlfg.github.io/prezero-clean/sim/kino.html>

Ausgeliefert wird `origin/master` → `sim/kino.html`; lokale Änderungen, die noch nicht nach GitHub übertragen sind, dort nicht sichtbar. Die Seite ist als Simulation gekennzeichnet, nicht als Messergebnis (`docs/KINO_VERTRAG.md`).

## Schnellstart

Voraussetzung: Python 3.11 oder neuer, pandas und NumPy. Die CSV muss lokal am Standardpfad liegen oder als Argument übergeben werden.

```bash
pip install "pandas>=2.0" "numpy>=1.24" pytest
python scripts/fakten.py
python scripts/fakten.py pfad/zur/datei.csv
python -m pytest tests/ -q
```

Ohne die lokale CSV laufen Fakten-Skript und Tests, die die Datei lesen, nicht. Alle Zahlen in diesem README zu den Messdaten stammen aus `scripts/fakten.py`.

## Daten

| Spalte | Bedeutung |
|---|---|
| `Location_id` | Container-Standort (anonym) |
| `material_type` | `brown`, `white`, `green` |
| `date` | Datum der Messung, ohne Uhrzeit |
| `fill_level_perc` | 0–100 in 10er-Stufen oder der Text `overfull` |

- 11.701 Messungen, keine fehlenden Werte, keine Duplikate, Zeitraum 17.10.2025 bis 30.09.2026 (348 Tage Differenz).
- 449 Container-IDs, 1.338 Kombinationen aus ID und Farbe. 441 IDs haben alle drei Farben, 7 haben zwei, 1 hat eine.
- Füllstand nie numerisch über 100. Überlauf steht als Text `overfull`: 1.192 Zeilen (10,2 %). Genau 100 %: 1.953 (16,7 %). Überlauf je Farbe: weiß 16,5 %, grün 8,6 %, braun 3,4 %.
- 4.468 Besuche (ID und Datum). Nur bei 3.061 wurden alle drei Farben gemessen, bei 1.111 zwei, bei 296 eine.
- Abstand zwischen Besuchen: Median 26 Tage, P10 12, P90 56, Maximum 222. Je ID Median 9 Besuche (1 bis 37).
- Der mittlere Füllstand steigt mit dem Abstand nur bis etwa 15–30 Tage (63,3 %) und bleibt danach flach. Der Überlaufanteil steigt weiter: 1,0 % bei höchstens 7 Tagen, 16,6 % bei mehr als 60 Tagen.
- Bilanz-Probe (Rate mal Abstand, in-sample): mittlerer Fehler 14,4 Prozentpunkte, 53,2 % der Fälle innerhalb von 10 Prozentpunkten. Das ist ein Befund; die festgelegten Grenzwerte stehen in `AGENTS.md`.

Ein Besuch ist als Paar (`Location_id`, `date`) definiert. Dass danach alle Farben auf 0 geleert werden, ist Annahme A1 in `AGENTS.md`, keine direkt beobachtete Gewissheit.

Abgeleitete Simulationsdaten liegen unter `data/derived/orte.json` (erzeugt von `scripts/sim_daten.py`).

## Modell und Tests

- `src/domaene.py` — Domänenmodell Glas, Container und LKW. Gate: `tests/test_domaene.py`.
- `src/modell.py` — Puffer-Modell je Kammer, Füllrate je `Location_id` und `material_type`. Gate: `tests/test_bilanz.py`.
- `tests/test_sim.py` — Tests zur Simulation.

Festgelegte Annahmen und Bilanz-Grenzwerte: `AGENTS.md`. Fachliche Beschreibung: `docs/modell.md` und `docs/datenmodell.md`.

## Weitere Befehle

```bash
python scripts/volumen_sensitivity.py
python scripts/bilder.py
```

Die vier Diagnose-Bilder `bilder/01_mechanismus.png`, `02_alle_orte.png`, `03_einheit.png` und `04_takt.png` entstehen aus denselben Daten. Erklärung: `bilder/LIESMICH.md`. Externe Volumenparameter: `docs/externe_parameter.md`.

Sensitivity aus internen Füllständen × externem Kammervolumen. Operative Annahme
**A6 (farbabhängig, AGENTS.md §3)**: white 3,2 / green 2,1 / brown 1,1 m³.
Quelle/Unsicherheit und festgehaltenes Ergebnis: `docs/externe_parameter.md` (V-1–V-4).

Das Simulations-Kino wird mit `scripts/kino_bauen.py` gebaut und lokal in `sim/kino.html` geöffnet.

## Simulation

`sim/kino.html` ist die Seite für den Stakeholder. Sie öffnet auf **1 · Ergebnis**:
Ersparnis an Leerungen gegenüber dem Ist-Lauf, mit der Überlaufquote als Wächter
und den Wegeinheiten als Aufwand, dazu je Parameter eine Tabelle. **2 · Verlauf**
zeigt die Simulation in Bewegung (Bühne, acht Kennzahlen, zwei Kurvenpanels),
**3 · Einstellen** die vier Hebel: Abstand, Autos, Strategie, Schwelle.

Jede sichtbare Zahl trägt einen **Herkunftsmarker** — `M` gemessen, `A` abgeleitet,
`S` gesetzt. Die Marker stehen in `meta.herkunft` (`scripts/sim_daten.py`), nicht im HTML.
Bewusst nicht enthalten: Kalender, Szenario-Dateien, LKW-Katalog, Temporegler —
sie beantworten keine Frage des Stakeholders.

```bash
python scripts/sim_daten.py    # Daten + Herkunftstags
python scripts/kino_bauen.py   # sim/kino.html bauen
```

Regeln und Marker-Tabelle: `docs/KINO_VERTRAG.md` Abschnitt 7.

## Zielzahl

Eingesparte Leerungen in Prozent gegenüber dem Ist-Plan, bei höchstens gleicher Überlaufquote. Ist-Basis aus den Daten: 4.468 Besuche, 10,2 % Überlauf-Messungen. Mehr Fahrten zählen nicht als Erfolg.

## Nicht im Scope

Geokoordinaten, Karten, Routing, Distanzen, Kosten, CO₂, Kraftstoff, LKW-Kapazität, Prognose-ML, Copilot, Pitch-Folien sowie gescrapte oder erfundene Zusatzdaten. Regeln: `SCOPE.md` und `assets/ui/UI_REGELN.md`.

## Offene Fragen an den Stakeholder (Marcel Fortuin, PreZero)

1. Ist ein Datensatz-Eintrag wirklich ein Besuch mit anschließender Leerung auf 0?
2. Warum fehlen bei 1.407 Besuchen eine oder zwei Farben: nicht gemessen oder nicht geleert?
3. Was bedeutet `overfull` genau, und wie viel Menge steckt dahinter?
4. Wie ist ein Besuch mit nur einem Tag Abstand (Minimum) zu erklären?
5. Was wäre aus Sicht von PreZero ein glaubwürdiger Wert für weniger Leerungen?

## Lizenz

Noch keine LICENSE-Datei; damit gelten zunächst alle Rechte vorbehalten.
