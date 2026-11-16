# 19 – Datenqualität bewerten

> Die CSV ist strukturell sauber (keine Nulls, keine Duplikate, keine ungültigen IDs), aber inhaltlich dünn: kein Messdatum exakt am Feiertag, nur ein Jahr, kategoriale Füllstände in 10%-Schritten und 10,2 % `overfull` ohne Höhenangabe.

## Frage

Wie gut ist der Datensatz, und welche Prüfungen fallen durch?

## Vorgehen

Systematische Qualitätsprüfung über fünf Dimensionen: Vollständigkeit, Wertebereich,
zeitliche Plausibilität, Konsistenz, Verlaufsplausibilität. Alle Zahlen direkt aus
`glass_fill_levels_anonymized_f.csv` (11.701 Zeilen, 449 Standorte, 1.338 Zeitreihen,
2025-10-17 bis 2026-09-30).

## Ergebnisse

### 1. Vollständigkeit

| Prüfung | Ergebnis |
|---|---:|
| Zeilen gesamt | 11.701 |
| Fehlende Werte je Spalte | 0 (alle vier Spalten vollständig) |
| Leere/ungültige Zeilen | 0 (11.702 Rohzeilen = 1 Header + 11.701 Daten) |
| Exakte Duplikate | 0 |
| Duplikate (gleicher Schlüssel Location + Material + Datum) | 0 |
| Schlüssel mit widersprüchlichem Wert | 0 |

### 2. Wertebereich

| Prüfung | Ergebnis |
|---|---:|
| Gültige Materialtypen (brown/green/white) | 100 % (3.100 / 4.169 / 4.432) |
| Ungültige Materialtypen | 0 |
| Ungültige `Location_id`-Formate | 0 (alle UUID-Format) |
| `fill_level_perc`-Werte außerhalb {0,10,…,100,overfull} | 0 |
| Messungen mit Wert 0 | 2 (0,02 %) |
| Messungen `overfull` (als 110 kodiert, Höhe unbekannt) | 1.192 (10,2 %) |
| `overfull`-Anteil je Material | braun 3,4 % · grün 8,6 % · weiß 16,5 % |

### 3. Zeitliche Plausibilität

| Prüfung | Ergebnis |
|---|---:|
| Messungen vor 2025-10-17 oder nach 2026-09-30 | 0 |
| Verschiedene Messtage | 229 |
| Zeitreihen mit mehreren Messungen am selben Tag | 0 |
| Doppelt gemessene Standorte (alle Materialien, gleicher Tag) | nicht beobachtet |

### 4. Konsistenz

| Prüfung | Ergebnis |
|---|---:|
| Standorte mit allen drei Materialien | 441 von 449 (98,2 %) |
| Standorte mit nur einem Material | 0 |
| Standorte mit nur einer Messung | 1 |
| Standorte mit < 5 Messungen | 12 (2,7 %) |
| Standorte mit ≥ 8 Messungen | 424 (94,4 %) |

### 5. Verlaufsplausibilität

| Prüfung | Ergebnis |
|---|---:|
| Übergänge gesamt | 10.363 |
| Positive Sprünge > 40 pp | 983 (9,5 %) |
| Negative Sprünge < −60 pp | 374 (3,6 %) |
| `overfull` → ≤ 40 % → `overfull` (Widerspruch) | 14 (0,1 %) |
| Zeitreihen mit SD > 40 pp (alle Kurzreihen, Median n = 3,5) | 32 (2,4 %) |
| Mod. Z-Score > 3,5 (Ausreißer) | 333 (3,1 % von 10.897 bewertbaren) |

### Scorecard (Ampel)

| Dimension | Bewertung |
|---|---|
| Vollständigkeit (keine Nulls/Duplikate) | 🟢 gut |
| Wertebereich/Konsistenz der Codes | 🟢 gut |
| Zeitliche Plausibilität | 🟢 gut (keine Zukunftswerte) |
| Repräsentativität der Standorte | 🟡 mittel (Messhäufigkeit 1–97, Median 24) |
| Verlaufsinformation (Leerungen nicht markiert) | 🔴 schlecht |
| Feiertags-/Tagesabdeckung | 🔴 schlecht (0 Messungen an allen 13 Feiertagen) |
| Kausalität (Ursachen) | 🔴 nicht aus CSV ableitbar |

### Die 5 wichtigsten Einschränkungen

1. **Leerungen sind nicht markiert** — nur indirekt über negative Sprünge rekonstruierbar.
2. **`overfull` hat keine Höhe** über 100 %; als 110 kodiert, echte Überfüllung unbekannt.
3. **Füllstände sind kategorial** in 10%-Schritten — feine Verläufe und exakte Raten
   sind nicht beobachtbar.
4. **Nur ein Jahr Daten** (2025-10 bis 2026-09) — Saison und Trend nicht trennbar.
5. **Keine echten Standortdaten** (Adresse, Koordinaten, Stadtteil, Gewerbe/Haushalte)
   und keine Leerungs-/Tourdaten.

## Grenzen

Die Prüfung bewertet nur die CSV selbst. Ob Messwerte korrekt sind, ob Sensoren
kalibriert waren, und ob `Location_id` wirklich einen Standort (und nicht einen
Container) bezeichnet, lässt sich aus der CSV nicht prüfen — das sind Fragen an
PreZero. Die Scorecard ist eine Einschätzung, keine zertifizierte Audit.

## Nächster Schritt

Die fünf Einschränkungen als Fragenliste für den PreZero-Mentor formalisieren
(vgl. Analyse 36) und im Prototypen als Datenvertrag dokumentieren, damit
keine Kennzahl aus der CSV überinterpretiert wird.