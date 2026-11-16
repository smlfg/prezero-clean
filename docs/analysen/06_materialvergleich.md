# 06 – Materialvergleich: Braun, Grün, Weiß

> Weißglas liegt an 429 von 441 Standorten mit allen drei Materialien über Braunglas (Median-Differenz 44 Prozentpunkte), die Rangfolge Braun < Grün < Weiß ist auf Standortebene eindeutig (Kruskal-Wallis H = 797,7; p ≈ 6·10⁻¹⁷⁴) – aber Braun streut relativ am stärksten, und der Abstand Grün–Weiß ist nur ein Drittel des Abstands Braun–Weiß.

## Frage

Wie unterscheiden sich Braun-, Grün- und Weißglas in Auslastungsniveau, Streuung und Verlauf – auf Messungs- und auf Standortebene – und sind die Unterschiede statistisch belastbar?

## Vorgehen

- Datengrundlage: `../glass_fill_levels_anonymized_f.csv`, 11.701 Messungen, 449 Standorte, 2025-10-17 bis 2026-09-30. `overfull` als 110 % kodiert (tatsächliche Höhe unbekannt).
- **Messungsebene:** n, Mittelwert, Median, Standardabweichung, Quartile, Anteil ≥ 80 %, `overfull`-Anteil, Anteil exakt 100 %, Messungen je Standort, typischer Messabstand.
- **Standortebene:** je Standort-/Material-Zeitreihe ein Mittelwert; darüber Anzahl Standorte, Mittel, Median, SD, Quartile, Variationskoeffizient, Anteil Standorte mit Ø ≥ 80 %, Anteil Standorte mit mindestens einem `overfull`.
- **Positive Rate:** Anteil positiver Schritte zwischen aufeinanderfolgenden Messungen einer Zeitreihe; mittlerer positiver Zuwachs, auf 30 Tage normiert.
- **Tests:** Kruskal-Wallis über Standort-Mittelwerte; paarweise Mann-Whitney U mit Cliff's Delta und Bonferroni (×3); auf der Teilmenge mit allen drei Materialien Friedman-Test und Wilcoxon-Vorzeichenrang mit Cohen's dz. Sensitivität: nur Standorte mit ≥ 5 bzw. ≥ 8 Messungen je Material.
- **Verlauf:** Quartalsmittel, zusätzlich auf balanciertem Panel (Zeitreihen mit Messung in allen vier Quartalen), monatliche Differenz Weiß − Braun, Steigung je Zeitreihe (pp/30 Tage).
- Werkzeug: `python3` mit pandas 3.0.3 und scipy 1.18.0.

## Ergebnisse

**Tabelle 1 – Messungsebene**

| Material | n | Mittel | Median | SD | Q25 | Q75 | ≥ 80 % | overfull | exakt 100 % | Messungen/Standort (Median) | Abstand (Tage) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Braun | 3.100 | 40,0 | 30 | 27,8 | 20 | 50 | 14,7 % | 3,4 % | 4,5 % | 6 | 33 |
| Grün | 4.169 | 68,1 | 70 | 27,7 | 40 | 90 | 43,8 % | 8,6 % | 16,1 % | 9 | 27 |
| Weiß | 4.432 | 82,2 | 90 | 24,0 | 70 | 100 | 66,5 % | 16,5 % | 25,7 % | 9 | 27 |

**Tabelle 2 – Standortebene (Aggregat der Standort-Mittelwerte)**

| Material | Standorte | Mittel | Median | SD | Q25 | Q75 | CV | Ø ≥ 80 % | ≥ 1× overfull | Messungen (min–max) |
|---|---|---|---|---|---|---|---|---|---|---|
| Braun | 442 | 37,7 | 36,1 | 15,7 | 26,0 | 47,2 | 41,8 % | 1,4 % (6) | 20,6 % | 1–26 |
| Grün | 448 | 65,4 | 66,7 | 14,6 | 55,3 | 76,2 | 22,3 % | 15,6 % (70) | 49,3 % | 1–35 |
| Weiß | 448 | 79,7 | 81,7 | 12,0 | 75,0 | 88,0 | 15,1 % | 60,0 % (269) | 73,2 % | 1–37 |

Auf Messungsebene sind die absoluten SD fast gleich (24–28 pp), weil die 10-pp-Rasterung und die Ränder (0/110) die Spanne begrenzen. Der Anteil ≥ 80 % unterscheidet sich dagegen um Faktor 4,5 (Braun zu Weiß).

**Tabelle 3 – Statistische Tests (Standort-Mittelwerte)**

| Test | Vergleich | Statistik | p | Effektstärke |
|---|---|---|---|---|
| Kruskal-Wallis | Braun/Grün/Weiß | H = 797,7 (df = 2) | 6,0·10⁻¹⁷⁴ | – |
| Mann-Whitney | Braun vs. Grün | U = 20.456 | 2,8·10⁻⁹³ | Cliff's δ = −0,79 |
| Mann-Whitney | Braun vs. Weiß | U = 5.846 | 2,1·10⁻¹³⁰ | Cliff's δ = −0,94 |
| Mann-Whitney | Grün vs. Weiß | U = 41.620 | 6,1·10⁻⁵² | Cliff's δ = −0,59 |
| Friedman (gepaart, n = 441) | alle drei | χ² = 711,8 (df = 2) | 2,7·10⁻¹⁵⁵ | – |
| Wilcoxon (gepaart) | Weiß vs. Braun | W = 75 | 2,8·10⁻⁷³ | dz = 2,63 |
| Wilcoxon (gepaart) | Grün vs. Braun | W = 1.608 | 1,3·10⁻⁶⁸ | dz = 1,61 |
| Wilcoxon (gepaart) | Weiß vs. Grün | W = 3.790 | 4,3·10⁻⁶² | dz = 1,16 |

**Tabelle 4 – Gepaarte Standorte (441 mit allen drei Materialien)**

| Kennzahl | Weiß − Braun | Grün − Braun | Weiß − Grün |
|---|---|---|---|
| Standort höher | 429 (97,3 %) | 408 (92,5 %) | 397 (90,0 %) |
| gleich / niedriger | 3 / 9 | 4 / 29 | 6 / 38 |
| Median-Differenz | 44,0 pp | 29,0 pp | 13,4 pp |
| Mittel-Differenz | 42,4 pp | 27,9 pp | 14,5 pp |
| 5 %- / 95 %-Quantil der Differenz | 13,5 / 64,4 pp | – | – |

Höchster Standort-Mittelwert: Weiß an 397, Grün an 42, Braun an 10 Standorten (7 Gleichstände). Sensitivität: nur Standorte mit ≥ 5 Messungen je Material (n = 306) → Median 38,5 / 69,2 / 83,6 pp, Weiß > Braun in 99,0 %; mit ≥ 8 Messungen (n = 169) → 41,2 / 72,0 / 86,4 pp, 98,8 %. Das Ergebnis ist nicht durch dünn besetzte Zeitreihen getragen.

**Tabelle 5 – Verlauf, Quartalsmittel (balanciertes Panel: 268 / 338 / 360 Zeitreihen)**

| Material | 2025 Q4 | 2026 Q1 | 2026 Q2 | 2026 Q3 |
|---|---|---|---|---|
| Braun | 29,8 | 51,6 | 53,2 | 35,8 |
| Grün | 67,6 | 84,0 | 65,3 | 63,0 |
| Weiß | 81,2 | 91,9 | 79,0 | 80,1 |
| Abstand Weiß − Braun | 51,4 | 40,3 | 25,8 | 44,3 |

Alle drei Materialien bewegen sich im Gleichschritt (Hoch im Winter/Frühjahr, Einbruch im Juni 2026, Erholung im Juli). Monatliche Differenz Weiß − Braun: zwischen 23,0 pp (März) und 53,8 pp (Dezember), Median 44,9 pp; kein Monat mit umgekehrtem Vorzeichen. Innerhalb der Zeitreihen (≥ 4 Messungen): Steigung +0,5 pp/30 Tage bei Braun, −1,6 bei Grün, −1,2 bei Weiß (Mediane +0,3 / −1,4 / −1,0). Positive Rate: 41 % / 42 % / 42 % der Schritte positiv; mittlerer positiver Zuwachs 28,1 / 36,9 / 33,6 pp je 30 Tage.

## Interpretation

- **Das Niveau ist der Unterschied, nicht die Schwankung.** Innerhalb einer Zeitreihe streuen alle drei Materialien ähnlich (Median der Reihen-SD 23,6 / 25,5 / 22,5 pp). Der Unterschied entsteht durch das Niveau: 37,7 vs. 65,4 vs. 79,7 pp im Standortmittel – ein fast konstanter Versatz.
- **Weißglas ist der Engpass.** 60 % der Standorte liegen im Mittel ≥ 80 %, 73 % hatten mindestens ein `overfull`, ein Viertel aller Messungen steht exakt auf 100 %. Wer nach einer einheitlichen Schwelle disponiert, plant überwiegend Weißglas-Touren.
- **Braun ist nicht „entspannt“, sondern unscharf gemessen.** Nur 442 Zeitreihen, median 6 Messungen, 134 Reihen mit weniger als 5 Werten, typischer Abstand 33 statt 27 Tage. Braun hat mit 41,8 % den höchsten relativen Streuungskoeffizienten – die Unsicherheit über den Standort liegt hier anteilig am höchsten.
- **Grün schwankt am stärksten im Wertebereich** (Q25–Q75 = 40–90, größter IQR aller Materialien): viele Behälter sind entweder fast leer oder fast voll, selten dazwischen. Für Rundtouren ist Grün damit der unzuverlässigste Einzelstandort-Prädiktor, im Mittel aber klar unter Weiß.
- **Der Versatz ist kein Messartefakt der Stichprobe:** Die gepaarten Tests (Friedman, Wilcoxon) bestätigen die Rangfolge an denselben 441 Standorten; die Sensitivitätsläufe mit ≥ 5 und ≥ 8 Messungen verschieben die Mediane nur um 1–4 pp.

## Grenzen

- `overfull` ist als 110 % kodiert, die tatsächliche Höhe ist unbekannt; dadurch ist der Weißglas-Mittelwert nach oben unscharf, und der Deckeneffekt (25,7 % exakt 100 %) drückt die Streuung künstlich.
- Kruskal-Wallis und Mann-Whitney setzen unabhängige Gruppen voraus; hier tritt derselbe Standort in mehreren Gruppen auf. Die p-Werte sind daher überzeichnet – die gepaarten Tests (Friedman, Wilcoxon) sind die belastbarere Grundlage, kommen aber zum gleichen Ergebnis.
- Messhäufigkeit korreliert mit dem Niveau (Spearman ρ = 0,33 / 0,37 / 0,39 für n gegen Standort-Mittel): häufiger angefahrene Standorte sind voller. Braun hat systematisch weniger Messungen – Niveauunterschiede können teils Auslastungs-, teils Erfassungsunterschied sein.
- Aggregate über Messtage sind durch die jeweils gemessene Teilmenge verzerrt; der Quartalsverlauf (Q4 2025 niedrig, Q1 2026 hoch, Juni-Einbruch) ist auch im balancierten Panel sichtbar, bleibt aber ohne Leerungsereignisse und Wetter nicht kausal deutbar. Saisonalität, Umstellung im Messbetrieb und Standortzuwachs sind nicht trennbar.
- 8 der 449 Standorte haben keine vollständige Materialkombination (6× Grün+Weiß, 1× Braun+Weiß, 1× nur Grün); Koordinaten sind synthetisch, räumliche Muster daher nicht prüfbar.
- Die 10-pp-Rasterung begrenzt die Auflösung der „positiven Rate“; Zuwächse unter 10 pp werden nur als Sprung zwischen Stufen sichtbar.

## Nächster Schritt

Für die 269 Standorte mit Weißglas-Mittelwert ≥ 80 % die Zeitreihen der letzten 90 Tage ziehen und zählen, wie viele ohne zwischenzeitliche Leerung drei oder mehr Messungen in Folge über 80 % bleiben – das trennt Dauervollstand von einem Artefakt der Messfrequenz.
