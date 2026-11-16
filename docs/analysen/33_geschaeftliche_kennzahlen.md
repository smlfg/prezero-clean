# 33 – Geschäftliche Kennzahlen erzeugen

> KPI-Set aus der CSV: mittlerer Füllstand 66,0 %, Überfüllungsquote 10,2 %,
> Anteil kritisch 44,7 %, 336 von 449 Standorten (74,8 %) mindestens einmal
> overfull, mittlere Füllrate 0,74 pp/Tag (≈ 27 Tage von 60 auf 80 %).

## Frage

Welche Kennzahlen eignen sich als Management- und Reporting-Größen?

## Vorgehen

Definition und Berechnung eines KPI-Sets aus der CSV, gruppiert in vier
Kategorien: Auslastung, Risiko, Dynamik, Datenqualität. Jede Kennzahl mit
Wert, Definition und Einheit. Empfehlung, welche Kennzahlen in ein Dashboard
gehören.

## Ergebnisse

### Kategorie A — Auslastung

| KPI | Wert | Definition |
|---|---:|---|
| Mittlerer Füllstand | 66,0 % | Mittel über alle Messungen |
| Median Füllstand | 70,0 % | Median über alle Messungen |
| Standortgleich gewichteter Mittelwert | 63,7 % | Mittel der Standortmittel |
| Anteil Standorte mit Mittelwert ≥ 80 % | 4,7 % | Standorte, chronisch hoch |
| Anteil Standorte mit Mittelwert < 50 % | 14,9 % | Standorte, chronisch niedrig |

### Kategorie B — Risiko

| KPI | Wert | Definition |
|---|---:|---|
| Überfüllungsquote | 10,2 % | Anteil overfull-Messungen |
| Anteil kritischer Messungen (≥ 80 %) | 44,7 % | Anteil ≥ 80 % |
| Anteil sehr kritischer Messungen (≥ 90 %) | 35,2 % | Anteil ≥ 90 % |
| Standorte mit ≥ 1 overfull-Messung | 74,8 % | 336 von 449 |
| Standorte mit overfull-Rate ≥ 20 % | 10,2 % | 46 von 449 |
| Material mit höchster overfull-Rate | Weißglas 16,5 % | vs. Grün 8,6 %, Braun 3,4 % |

### Kategorie C — Dynamik

| KPI | Wert | Definition |
|---|---:|---|
| Median Füllrate (positiv) | 0,74 pp/Tag | Median der Zuwachsraten |
| Tage von 60 auf 80 % | ≈ 27 | bei Median-Rate |
| Tage von 80 auf 100 % | ≈ 27 | bei Median-Rate |
| Median Messabstand | 28 Tage | zwischen zwei Messungen |
| Messungen pro Zeitreihe (Median) | 8 | pro Standort/Material |
| Zeitreihen mit ≥ 8 Messungen | 708 von 1.338 | 52,9 % |

### Kategorie D — Datenqualität

| KPI | Wert | Definition |
|---|---:|---|
| Messabdeckung (Median/Standort) | 24 Messungen | je Standort |
| Standorte mit < 5 Messungen | 12 (2,7 %) | geringe Evidenz |
| Fehlende Werte | 0 | alle Spalten vollständig |
| Duplikate | 0 | keine Dubletten |
| Messtage | 229 | verschiedene Tage |
| Feiertage mit Messung | 0 | alle 13 Feiertage leer |

### Kategorie E — Servicequalität (vorgeschlagen)

| KPI | Wert | Definition |
|---|---:|---|
| Service-Score (0–100) | 64,4 | 100 − (overfull-Rate × 2 + kritische-Rate × 0,5) |
| Zielwert (guter Monat, z. B. Juni) | 84,9 | 100 − (5,2 × 2 + 24,7 × 0,5) |
| Kritische Stopps/Tag (Median) | 13 | Standorte ≥ 80 % an einem Messtag |
| Kritische Stopps/Tag (Spitze) | 40 | Maximum über alle Messtage |

### Empfehlung für das Dashboard (Analyse 34)

Mindestens diese 8 KPIs sollten prominent stehen: mittlerer Füllstand,
Überfüllungsquote, Anteil kritisch, Standorte mit overfull, Service-Score,
kritische Stopps/Tag, Median-Messabstand, Messungen/Zeitreihe. Alle anderen
als Drill-down.

## Grenzen

KPIs sind nur so gut wie die Messung. Weil Messabstände median 28 Tage
betragen und Feiertage leer sind, sind die Kennzahlen Momentaufnahmen der
gemessenen Teilmenge, nicht des Gesamtbestands. Trendaussagen über ein Jahr
sind nicht signifikant.

## Nächster Schritt

KPI-Set mit dem Mentor abstimmen und als Vertrag (welche Kennzahl, welche
Definition, welcher Zeitraum) dokumentieren, damit Dashboard und Reporting
dieselben Zahlen zeigen.