# Kontext für alle Analysen (verbindlich)

Diese Datei ist die gemeinsame Grundlage für alle 36 Einzelanalysen in diesem Ordner.
Jede Analyse ist **eine Datei**, geschrieben von genau einem Subagenten.

## Datengrundlage

| Datei | Inhalt |
|---|---|
| `../glass_fill_levels_anonymized_f.csv` | Füllstandsmessungen, 11.701 Zeilen |
| `../locations_synthetic.csv` | 449 synthetische Koordinaten (`source=synthetic_placeholder`) |

Spalten der Messdatei: `Location_id`, `material_type`, `date`, `fill_level_perc`.

## Belegte Datenfakten (nicht neu erfinden, aber gern nachrechnen)

- Zeitraum: 2025-10-17 bis 2026-09-30, 229 verschiedene Messtage.
- 449 `Location_id`, 1.338 Standort-/Material-Zeitreihen.
- Materialien: `white` 4.432, `green` 4.169, `brown` 3.100 Messungen.
- `fill_level_perc` ist **kategorial**: 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, `overfull`
  (nur 2 Messungen mit 0, 1.192 `overfull` = 10,2%).
- Messungen pro Zeitreihe: min 1, Median 8, max 37. Typischer Abstand ≈ 41 Tage.
- Mittelwerte: braun 40,0% · grün 68,1% · weiß 82,2%.
- Anteil ≥ 80%: braun 14,7% · grün 43,8% · weiß 66,4%.
- `overfull`-Anteil: braun 3,4% · grün 8,6% · weiß 16,5%.

## Konventionen

- `overfull` wird für numerische Rechnungen als **110** kodiert. Im Text immer
  schreiben: „overfull (als 110% kodiert, tatsächliche Höhe unbekannt)“.
- Ein **negativer Sprung** ist ein Indiz für Leerung/Reset, kein Beweis.
- `Location_id` bezeichnet einen **Standort** (mehrere Materialbehälter), nicht
  zwingend einen einzelnen physischen Container.
- Koordinaten sind **synthetisch**. Niemals als echte Adresse darstellen.
- Aggregate über Messtage sind durch die jeweils gemessene Teilmenge verzerrt.
  Das in den Grenzen nennen.

## Aufbau jeder Datei (verbindlich)

```markdown
# NN – <Titel>

> Ein-Satz-Kernaussage mit der wichtigsten Zahl.

## Frage
## Vorgehen        (Methode, Filter, Kennzahlen, kurz)
## Ergebnisse      (Tabellen + konkrete Zahlen aus der CSV)
## Interpretation  (was das operativ bedeutet)
## Grenzen         (Datenlücken, Kausalität, Anonymisierung)
## Nächster Schritt (genau einer)
```

## Regeln

1. **Jede Zahl muss aus der CSV berechnet sein.** Keine Schätzungen, keine
   erfundenen Werte. Rechne mit `python3` + `pandas` (installiert) im Ordner `PreZero/`.
2. Kurz und dicht: 60–140 Zeilen. Tabellen statt Prosa.
3. Deutsch, sachlich. Keine Werbe-Sprache.
4. Grenzen sind Pflicht, nicht Deko. Wo die Daten keine Kausalität hergeben, das sagen.
5. Wenn eine Analyse zusätzliche Daten bräuchte (Adressen, Leerungsereignisse,
   Wetter, Fahrzeugkapazität): klar benennen, was fehlt und was man damit könnte.
6. Nicht die anderen Analysedateien zusammenfassen — jede Datei steht für sich.
