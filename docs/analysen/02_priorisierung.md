# 02 – Container priorisieren: Rangliste aus Füllstand, Auslastung und Füllrate

> Ein transparenter Score aus letztem Messwert (50 %), positiver Füllrate (30 %) und Zeitreihen-Mittel (20 %) setzt **19 Serien über 90 Punkte** und 101 über 80; **117 von 1.338 Zeitreihen sind nicht bewertbar** (81 mit < 3 Messungen, 36 ohne steigendes Intervall).

## Frage

Wie lässt sich aus aktuellem Füllstand, historischer Auslastung und Anstiegsgeschwindigkeit eine belastbare Rangliste für die nächste Leerung erstellen?

## Vorgehen

- Eine Zeitreihe = `Location_id` × `material_type`: 1.338 Serien aus 11.701 Messungen (2025-10-17 bis 2026-09-30). `overfull` wird als 110 kodiert (tatsächliche Höhe unbekannt).
- **Letzter Messwert**: jüngste Messung der Serie, 0–110.
- **Mittlerer Füllstand**: arithmetisches Mittel aller Messungen der Serie, 0–110.
- **Positive Füllrate**: für jedes aufeinanderfolgende Messpaar einer Serie mit Δt > 0 wird ΔFüllstand/Δt gebildet; gemittelt werden nur die **positiven** Werte (negative Sprünge sind Indiz für Leerung/Reset und werden verworfen, nicht als Abfall interpretiert).
- **Bewertbar** ist eine Serie nur mit ≥ 3 Messungen **und** ≥ 1 positivem Intervall. Alles andere wird nicht gescort, sondern gezählt.
- Normierung: die drei Komponenten werden auf 0–100 gebracht, damit Gewichte vergleichbar sind.

| Komponente | Rohwert | Normierung | Warum so |
|---|---|---|---|
| Letzter Messwert | 0–110 | `Wert / 110 × 100` | natürliche Obergrenze der Skala, kein Clipping nötig |
| Mittlerer Füllstand | 0–110 | `Wert / 110 × 100` | gleiche Skala, direkt vergleichbar |
| Füllrate | pp/Tag | `min(Rate / 2,05, 1) × 100` | Verteilung ist rechtsschief (Median 0,77 · P95 2,05 · Max 13,31 pp/Tag); ohne Kappung bei P95 würde ein einzelner Ausreißer die Komponente dominieren |

**Gewichte (G1, Hauptvariante):** 0,50 · 0,30 · 0,20.

| Komponente | Gewicht | Begründung |
|---|---|---|
| Letzter Messwert | 0,50 | entscheidet operativ, ob der Behälter bis zur nächsten Tour überläuft — höchste Dringlichkeitsaussage |
| Positive Füllrate | 0,30 | prognostisch: wie schnell erreicht die Serie wieder die Grenze; weniger sicher als der Ist-Wert, weil aus wenigen Intervallen |
| Mittlerer Füllstand | 0,20 | strukturelles Niveau, dämpft Einzelmessungs-Rauschen; sagt aber nicht, wie es *jetzt* steht, daher geringstes Gewicht |

**Sensitivitätscheck:** G2 = gleichgewichtet (0,34 / 0,33 / 0,33), G3 = rate-betont (0,30 / 0,50 / 0,20). Vergleich über Spearman-Rangkorrelation auf allen bewertbaren Serien und Überlappung der Top-25.

## Ergebnisse

### Bewertbarkeit

| Kategorie | Serien |
|---|---|
| Zeitreihen gesamt | 1.338 |
| bewertbar (≥ 3 Messungen, ≥ 1 positives Intervall) | 1.221 |
| **nicht bewertbar** | **117** |
| davon < 3 Messungen | 81 |
| davon ≥ 3 Messungen, aber kein positives Intervall (nur fallend/Reset) | 36 |

Median Messungen je bewertbarer Serie: 9; Median positive Füllrate 0,77 pp/Tag.

### Top 25 nach Score G1

`110*` = overfull (als 110 % kodiert, tatsächliche Höhe unbekannt). `n` = Messungen der Serie.

| # | Standort | Material | letzter Wert | Datum | Mittel | Rate (pp/Tag) | n | Score |
|---|---|---|---|---|---|---|---|---|
| 1 | `df6d6307` | green | 110* | 2026-09-28 | 94,7 | 2,34 | 15 | 97,2 |
| 2 | `eecbf6fa` | white | 110* | 2026-09-29 | 91,0 | 2,12 | 29 | 96,6 |
| 3 | `df6d6307` | white | 110* | 2026-09-28 | 89,3 | 2,71 | 15 | 96,2 |
| 4 | `80b7f22a` | green | 110* | 2026-09-28 | 88,2 | 2,34 | 17 | 96,0 |
| 5 | `5e5cb60f` | white | 110* | 2026-09-16 | 88,2 | 2,03 | 17 | 95,7 |
| 6 | `1d4f4d33` | white | 110* | 2026-09-29 | 84,4 | 3,05 | 25 | 95,3 |
| 7 | `8407541b` | white | 110* | 2026-09-28 | 84,0 | 2,42 | 10 | 95,3 |
| 8 | `20e4dd82` | white | 110* | 2026-09-09 | 78,2 | 3,39 | 17 | 94,2 |
| 9 | `eecbf6fa` | green | 110* | 2026-09-29 | 77,2 | 2,47 | 29 | 94,0 |
| 10 | `6585283f` | white | 100 | 2026-06-12 | 97,8 | 2,33 | 9 | 93,2 |
| 11 | `20e4dd82` | green | 110* | 2026-09-09 | 71,2 | 3,11 | 17 | 92,9 |
| 12 | `1d4f4d33` | green | 110* | 2026-09-29 | 66,0 | 2,47 | 25 | 92,0 |
| 13 | `5bdc5e59` | white | 110* | 2026-09-30 | 81,9 | 1,85 | 16 | 92,0 |
| 14 | `cb52636c` | green | 110* | 2026-09-29 | 84,2 | 1,82 | 19 | 91,8 |
| 15 | `4d95737e` | white | 110* | 2026-09-29 | 83,0 | 1,77 | 27 | 90,9 |
| 16 | `fd2c8a46` | white | 100 | 2026-09-10 | 85,0 | 2,89 | 16 | 90,9 |
| 17 | `1e82edc0` | green | 110* | 2026-09-29 | 85,7 | 1,73 | 23 | 90,8 |
| 18 | `5ff0f0b3` | white | 100 | 2026-09-11 | 81,2 | 2,34 | 17 | 90,2 |
| 19 | `eecbf6fa` | brown | 110* | 2026-09-29 | 55,5 | 2,48 | 22 | 90,1 |
| 20 | `c7208f1a` | green | 100 | 2026-09-09 | 87,3 | 1,95 | 15 | 89,9 |
| 21 | `511d53a1` | white | 100 | 2026-09-16 | 76,5 | 2,82 | 17 | 89,4 |
| 22 | `a587ad61` | white | 100 | 2026-09-14 | 85,9 | 1,94 | 29 | 89,3 |
| 23 | `fe3b230b` | green | 110* | 2026-09-29 | 77,1 | 1,73 | 14 | 89,2 |
| 24 | `05c3c6dc` | green | 110* | 2026-08-31 | 70,6 | 1,80 | 17 | 89,1 |
| 25 | `de821fab` | white | 110* | 2026-09-30 | 93,8 | 1,49 | 8 | 88,9 |

### Verteilung und Zusammensetzung

| Kennzahl | Wert |
|---|---|
| Score-Spanne (bewertbar) | 8,3 – 97,2 |
| Median / P90 | 52,2 / 78,5 |
| Serien ≥ 90 / ≥ 80 Punkte | 19 / 101 |
| Top-25: Anteil overfull | 19 von 25 |
| Top-25: Materialverteilung | white 14 · green 10 · brown 1 |
| Top-25: verschiedene Standorte | 20 (4 Standorte mit 2–3 Serien) |
| Top-25: Median Tage seit letzter Messung | 2 (alle bewertbaren Serien: 21) |
| Top-25: Rang 25 vs. Rang 26 | 88,9 vs. 88,8 Punkte |

Komponenten-Rangkorrelationen: letzter Wert ↔ Mittel 0,74 · letzter Wert ↔ Rate 0,30 · Mittel ↔ Rate 0,35 — die drei Komponenten tragen unterschiedliche Information; die Rate ist am wenigsten redundant.

### Sensitivitätscheck

| Variante | Gewichte (letzter Wert / Rate / Mittel) | Spearman ρ vs. G1 | Top-25-Überlappung mit G1 |
|---|---|---|---|
| G1 (Haupt) | 0,50 / 0,30 / 0,20 | — | 25 / 25 |
| G2 gleichgewichtet | 0,34 / 0,33 / 0,33 | 0,990 | 22 / 25 |
| G3 rate-betont | 0,30 / 0,50 / 0,20 | 0,944 | 20 / 25 |

Zum Vergleich: eine Rangliste nur nach letztem Messwert hat ρ = 0,918 zu G1, überlappt aber nur in 6 von 25 Fällen — der Score ist keine umbenannte Ist-Wert-Liste. Die Rangfolge ist gegen die Gewichtswahl robust (ρ ≥ 0,94), die *Auswahl* der letzten Plätze ist es nicht: bei 88,8 vs. 88,9 Punkten entscheidet die Nachkommastelle.

## Interpretation

- **Sofortmaßnahme:** 19 Serien liegen bei ≥ 90 Punkten; 19 der Top-25 stehen auf overfull, und die Top-25 wurden im Median 2 Tage vor dem Stichtag gemessen. Diese Gruppe ist ohne weitere Modellierung leerungsreif.
- **Zwei Signale, zwei Fälle:** `df6d6307` (green, 97,2) steht bei 110 und hat zusätzlich Mittel 94,7 — dauerhaft voll, nicht Ausreißer. `6585283f` (white, 93,2) steht nur bei 100, hat aber Mittel 97,8 und Rate 2,33 — ebenfalls strukturell voll, obwohl die letzte Messung vom 2026-06-12 stammt.
- **Braun ist kein Sonderfall, sondern unterrepräsentiert:** 1 von 25 Top-Serien bei 31,6 % Anteil an den bewertbaren Serien — konsistent mit dem niedrigen Braun-Niveau (40,0 % Mittelwert). Braune Behälter konkurrieren im gemeinsamen Score selten um vordere Plätze; wer Materialprioritäten setzt, muss das explizit tun.
- **Raten sind niedrig:** Median 0,77 pp/Tag heißt ~13 Tage von 50 auf 60 %. Bei typischem Messabstand von 41 Tagen ist der Füllstand zwischen zwei Messungen praktisch immer überholt; die Rate ist eine Größenordnung, kein Forecast.

## Grenzen

- **Keine Leerungsdaten.** Negative Sprünge werden als Reset interpretiert, sind aber nicht belegt; ein echter Rückgang (z. B. Verdichtung, Messfehler) würde die Rate verfälschen. Ohne Leerungsereignisse ist die Rate eine Obergrenze der Füllgeschwindigkeit.
- **Stichtag 2026-09-30 ist für alle Serien gesetzt**, die letzte Messung liegt im Median 21 Tage davor. Ein hoher Score auf alter Messung ist eine Hypothese, keine Momentaufnahme; das Datum steht deshalb in der Tabelle.
- **Füllstand ist kategorial** (10er-Schritte). Raten aus 10er-Sprüngen sind grob quantisiert; eine Rate von 2,34 pp/Tag heißt „eine 10-pp-Stufe in 4 Tagen" — eine Größenordnung, kein präziser Wert.
- **`overfull` = 110 ist eine Untergrenze.** Tatsächliche Höhe unbekannt, Überlauf nicht messbar; overfull-Serien werden im Score gleich behandelt, obwohl sie sich real unterscheiden.
- **`Location_id` ist ein Standort, kein Container.** Mehrere Materialbehälter am selben Standort werden getrennt gescort, obwohl eine Tour sie gemeinsam anfährt; Kapazität, Volumen und Behältergröße fehlen komplett.
- **Score ist relativ, nicht absolut.** Ein Score von 95 heißt „dringlicher als andere Serien im Datensatz", nicht „läuft morgen über". Ein absoluter Schwellenwert bräuchte Kapazität, Tourenplan und Zeit seit letzter Leerung.
- Koordinaten sind synthetisch; die Rangliste lässt sich nicht in eine Route übersetzen.

## Nächster Schritt

Score-Gewichte mit echten Leerungsereignissen kalibrieren: sobald für einen Teil der Standorte Tourdaten vorliegen, prüfen, ob hohe G1-Werte tatsächlich vor der Leerung standen (Precision@25), und erst dann die Gewichte festschreiben.
