# PreZero Glascontainer – sauberer Neustart (nur Daten)

## Problem in drei Sätzen
Ein Glascontainer ist ein Puffer: Er füllt sich von selbst, und ein LKW-Besuch leert ihn wieder auf 0.
Bei jedem Besuch liest der Fahrer den Füllstand ab, danach wird geleert (Annahme, siehe AGENTS.md).
Gesucht ist ein Plan, der Überlauf vermeidet, **ohne mehr zu fahren**.

## Die Daten (alle Zahlen aus `scripts/fakten.py`)
Datei: `data/glass_fill_levels_anonymized_f.csv` (kann vertraulich sein, nicht veröffentlichen).

| Spalte | Bedeutung |
|---|---|
| `Location_id` | Container-Standort (anonym) |
| `material_type` | `brown`, `white`, `green` |
| `date` | Datum der Messung, **ohne Uhrzeit** |
| `fill_level_perc` | 0–100 in 10er-Stufen, oder Text `overfull` |

- **11.701 Messungen**, keine fehlenden Werte, keine Duplikate, 17.10.2025 bis 30.09.2026 (348 Tage).
- **449 Container-IDs**, 1.338 Kombinationen ID+Farbe. 441 IDs haben alle 3 Farben, 7 haben 2, 1 hat 1.
- **Füllstand:** nie numerisch über 100. Überlauf steht als Text `overfull`: 1.192 Zeilen (10,2 %). Genau 100 %: 1.953 (16,7 %).
  Überlauf je Farbe: weiß 16,5 %, grün 8,6 %, braun 3,4 %.
- **4.468 Besuche** (ID+Datum). Nur bei 3.061 wurden alle 3 Farben gemessen, bei 1.111 zwei, bei 296 eine.
- **Abstand zwischen Besuchen:** Median 26 Tage, P10 12, P90 56, Maximum 222. Je ID Median 9 Besuche (1 bis 37).
- Füllstand steigt mit dem Abstand nur bis etwa 15–30 Tage (Mittel 63 %) und bleibt dann flach. Überlauf steigt weiter (1 % bei ≤ 7 Tagen, 17 % bei > 60).
- Bilanz-Probe (Rate × Abstand): mittlerer Fehler 14,4 Prozentpunkte, 53 % der Fälle innerhalb 10 Pp. Das ist ein Befund, kein bestandener Test.

## Nicht im Scope
Geokoordinaten, Karten, Routing, Distanzen, Kosten, CO₂, Kraftstoff, LKW-Kapazität, Prognose-ML, UI, Copilot, Pitch-Folien, gescrapte oder erfundene Zusatzdaten.

## Die eine Zielzahl
**Eingesparte Leerungen in % gegenüber dem Ist-Plan, bei höchstens gleicher Überlaufquote.**
Ist-Basis aus den Daten: 4.468 Besuche, 10,2 % Überlauf-Messungen. Mehr Fahrten zählen nie als Erfolg.

## Phasen (jede erst nach der vorigen)
1. **Daten verstehen und visualisieren:** `fakten.py`, Verteilungen, Füllkurven je Container und Farbe. Nur Diagramme, keine App.
2. **Modell:** Container = Puffer mit Füllrate je ID (und Farbe), Besuch = Leerung auf 0. Annahmen benennen.
3. **Bilanztest:** Grenzwerte festlegen und grün bekommen (siehe AGENTS.md).
4. **Optimieren:** Besuchsabstände je Container so wählen, dass Zielzahl besser wird. Backtest nur auf späteren Daten als dem Training.

## Offene Fragen an den Stakeholder (Marcel Fortuin, PreZero)
1. Ist ein Datensatz-Eintrag wirklich ein Besuch mit anschließender Leerung auf 0?
2. Warum fehlen bei 1.407 Besuchen eine oder zwei Farben: nicht gemessen oder nicht geleert?
3. Was bedeutet `overfull` genau, und wie viel Menge steckt dahinter?
4. Wie ist ein Besuch mit nur 1 Tag Abstand (Minimum) zu erklären?
5. Was wäre aus Sicht von PreZero ein glaubwürdiger Wert für „weniger Leerungen“?
