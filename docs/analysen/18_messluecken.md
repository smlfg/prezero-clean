# 18 – Unregelmäßige Messungen erkennen

> Jede dritte der 1.338 Zeitreihen (458, 34,2%) hat mindestens eine Lücke über 90 Tage, und 256 Reihen (19,6%) sind für Prognosen praktisch unbrauchbar – Braunglas ist mit 32,4% schlecht prognostizierbarer Reihen der Problemfall.

## Frage

Bei welchen Zeitreihen sind Prognosen wegen großer Zeitlücken besonders unsicher? Wie unregelmäßig wird gemessen, sind die Lücken systematisch (Kalender, Wochentag, Feiertage), und hängt die Messhäufigkeit eines Standorts mit seinem Füllstand zusammen?

## Vorgehen

- Datengrundlage: `glass_fill_levels_anonymized_f.csv` (11.701 Messungen, 1.338 Standort-/Material-Zeitreihen, 229 Messtage, 349 Kalendertage vom 2025-10-17 bis 2026-09-30).
- **Abstand** = Kalendertage zwischen zwei aufeinanderfolgenden Messungen *derselben* Zeitreihe (`Location_id` + `material_type`). 1.338 Reihen ergeben 10.363 Intervalle; 34 Reihen mit nur einer Messung liefern kein Intervall.
- Verteilung über alle Intervalle (nicht pro Reihe gemittelt), damit jede Lücke gleich zählt.
- **Unsicherheits-Score** (0 = sicher, 1 = unsicher): `Score = 0,5 · (1 − min(n,12)/12) + 0,5 · min(max_gap,180)/180` mit `n` = Anzahl Messungen, `max_gap` = längste Lücke der Reihe. Beide Terme sind auf 0…1 gekappt, damit Ausreißer nicht alles dominieren. Klassen: **gut** < 0,30 · **mittel** 0,30–0,60 · **schlecht** ≥ 0,60.
- Kalenderprüfung: alle 13 baden-württembergischen Feiertage im Zeitraum einzeln abgefragt; Monats-, Wochentags- und Tagesverteilung.
- Füllstand: `overfull` als 110% kodiert (tatsächliche Höhe unbekannt). Zusammenhang Häufigkeit↔Füllstand sowohl im Querschnitt (Spearman-Rangkorrelation) als auch *innerhalb* der Zeitreihe geprüft.

## Ergebnisse

### Verteilung der Messabstände (10.363 Intervalle)

| Kennzahl | Tage |
|---|---|
| Minimum | 1 |
| Q1 | 18 |
| Median | 28 |
| Q3 | 42 |
| p90 | 69 |
| p95 | 90 |
| p99 | 155 |
| Maximum | 272 |

| Schwelle | Intervalle darüber | Anteil |
|---|---|---|
| > 14 Tage | 8.767 | 84,6% |
| > 30 Tage | 4.494 | 43,4% |
| > 60 Tage | 1.282 | 12,4% |
| > 90 Tage | 518 | 5,0% |
| > 120 Tage | 223 | 2,2% |

Der Median-Abstand von 28 Tagen und der mittlere Reihen-Rhythmus (`Spanne / (n−1)`) von 41 Tagen fallen auseinander, weil die Verteilung rechtsschief ist: die Hälfte der Abstände ist kurz, ein langer Schwanz zieht den Mittelwert. **Keine einzige Reihe** hat eine maximale Lücke unter 20 Tagen; der Median der längsten Lücke liegt bei 76 Tagen – ein durchgehend regelmäßiger Takt existiert im Datensatz nicht.

### Betroffenheit auf Reihenebene (1.338 Reihen)

| Lücke überschreitet | Reihen | Anteil aller 1.338 |
|---|---|---|
| 30 Tage | 1.270 | 94,9% |
| 60 Tage | 866 | 64,7% |
| 90 Tage | **458** | **34,2%** |
| 120 Tage | 217 | 16,2% |

### Unsicherheits-Score und Klassen

| Klasse | Reihen | Anteil* | Median n | Median max. Lücke | Median Mittel-Füllstand |
|---|---|---|---|---|---|
| gut | 510 | 39,1% | 13 | 50 Tage | 77,3% |
| mittel | 538 | 41,3% | 7 | 83 Tage | 60,0% |
| schlecht | 256 | 19,6% | 4 | 147 Tage | 45,5% |
| nicht bewertbar (n = 1) | 34 | — | 1 | — | — |

\*Anteil an den 1.304 bewertbaren Reihen.

Nach Material:

| Material | Reihen | Median n | Median max. Lücke | Anteil „schlecht“ |
|---|---|---|---|---|
| brown | 442 | 6 | 95 Tage | 32,4% |
| green | 448 | 9 | 71 Tage | 16,2% |
| white | 448 | 9 | 60 Tage | 10,9% |

Auch die Intervalle selbst unterscheiden sich: Median 33 Tage (braun) gegen 27 Tage (grün/weiß), Anteil Intervalle > 60 Tage 21,5% (braun) gegen 10,5% / 8,1%.

### Systematik: Kalender und Wochentag

- 229 Messtage = 212 Werktage + 11 Samstage + 6 Sonntage. Von 239 Werktagen (ohne Feiertage) wurde an 212 gemessen = **88,7%**; 120 der 349 Kalendertage bleiben ohne jede Messung.
- **Alle 13 geprüften Feiertage haben exakt 0 Messungen** (u. a. 2025-11-01, 2025-12-25/26, 2026-01-01, 2026-01-06, Karfreitag 2026-04-03, 2026-05-01, 2026-06-04). Der 24.12. (39) und 31.12. (66) wurden dagegen normal bedient.
- Wochentage: Mo 1.959 · Di 2.315 · **Mi 2.563** · Do 2.222 · Fr 2.177 · Sa 444 · So 21. Wochenende = 4,0% aller Messungen; Sonntage sind faktisch ausgeschlossen.
- Messungen pro Messtag schwanken zwischen 33,7 (März 2026) und 71,5 (Juni 2026) – ein Faktor 2,1 bei gleicher Tageszahl.
- Große Lücken (> 60 Tage) *beginnen* überproportional im Winter: Dez 2025 303, Jan 2026 175, Feb 2026 202 – zusammen mit Okt/Nov 2025 rund 70% aller 1.282 großen Lücken.
- **62,6%** der Lücken > 60 Tage treten standortweit auf: mindestens zwei Materialien desselben Standorts fehlen mit identischem Start- und Endtag. Das sind 809 verschiedene ausgelassene Standort-Zeiträume, nicht 1.282 materialbedingte Einzelfälle.

### Füllstand und Messhäufigkeit

Querschnitt über die Reihen: Spearman-Rangkorrelation Anzahl Messungen ↔ mittlerer Füllstand = **+0,41** (braun +0,33, grün +0,38, weiß +0,42). Der Gradient ist monoton:

| Messungen je Reihe | ≤3 | 4–5 | 6–7 | 8–9 | 10–11 | 12–15 | >15 |
|---|---|---|---|---|---|---|---|
| Mittel braun | 33,2 | 32,8 | 37,6 | 40,5 | 45,0 | 43,2 | 44,8 |
| Mittel grün | 58,6 | 60,1 | 60,4 | 66,0 | 66,4 | 72,6 | 72,5 |
| Mittel weiß | 71,7 | 73,6 | 75,5 | 79,4 | 82,1 | 85,1 | 86,0 |

Innerhalb einer Zeitreihe verschwindet der Effekt jedoch: der Median des *nächsten* Abstands beträgt 21 Tage in allen drei Füllstandsgruppen (≤40% n=1.483; 50–80% n=2.256; ≥90% n=2.651), und bei 364 Reihen mit beiden Extremen ist der Abstand nach niedrigem Füllstand sogar 3 Tage kürzer (nur 35,7% der Reihen zeigen das erwartete Muster „voll → früher wieder“).

### Top-20 Zeitreihen mit den größten Lücken

| # | Standort (8 Zeichen) | Material | von | bis | Lücke | Füllstand danach |
|---|---|---|---|---|---|---|
| 1 | fe0e3e24 | brown | 2025-10-30 | 2026-07-29 | 272 | 60% |
| 2 | 6f32b496 | brown | 2025-11-06 | 2026-07-29 | 265 | 20% |
| 3 | f019215f | brown | 2025-12-09 | 2026-08-25 | 259 | 70% |
| 4 | e53aeac2 | brown | 2025-10-31 | 2026-07-16 | 258 | 40% |
| 5 | bf290a6e | brown | 2025-11-06 | 2026-07-21 | 257 | 10% |
| 6 | f306348d | brown | 2025-12-10 | 2026-08-10 | 243 | 30% |
| 7 | 65c6ad0a | brown | 2025-10-17 | 2026-06-10 | 236 | 20% |
| 8 | 7346dabb | brown | 2025-12-19 | 2026-08-07 | 231 | 20% |
| 9 | 7346dabb | green | 2025-12-19 | 2026-08-07 | 231 | 10% |
| 10 | 8725bd5e | brown | 2025-12-10 | 2026-07-22 | 224 | 60% |
| 11 | 43ff3a23 | brown | 2025-10-30 | 2026-06-09 | 222 | 20% |
| 12 | 43ff3a23 | green | 2025-10-30 | 2026-06-09 | 222 | 50% |
| 13 | 43ff3a23 | white | 2025-10-30 | 2026-06-09 | 222 | 70% |
| 14 | bca715c6 | brown | 2025-12-02 | 2026-07-07 | 217 | 10% |
| 15 | 382ea508 | brown | 2025-11-06 | 2026-06-06 | 212 | 40% |
| 16 | 3b580eae | brown | 2025-11-06 | 2026-06-06 | 212 | 40% |
| 17 | 3b580eae | green | 2025-11-06 | 2026-06-06 | 212 | 100% |
| 18 | 734f7e77 | brown | 2026-01-27 | 2026-08-27 | 212 | 30% |
| 19 | 77ba55cc | brown | 2025-12-30 | 2026-07-29 | 211 | 30% |
| 20 | eed9b1bb | brown | 2025-11-07 | 2026-06-05 | 210 | 40% |

Auffällig: **alle 20 Extremfälle sind Braunglas-Reihen** (Nr. 9, 12, 13, 17 sind die Mitreißer desselben Standorts), und alle 20 gehören der Klasse „schlecht“ an. Es sind Reihen mit nur 2–4 Messungen, keine Reihen mit einem einzelnen Ausrutscher.

## Interpretation

- **Prognosefähig ist nur ein Kern von rund 40%.** 510 Reihen mit ≥ 8–13 Messungen und maximalen Lücken um 50 Tage tragen eine belastbare Zeitreihe. Die 256 „schlechten“ Reihen (19,6%) haben im Median 4 Messungen und 147 Tage Lücke – dort ist jede Trend- oder Saisonprognose Spekulation, sinnvoll ist nur eine konservative Bandbreite oder ein Materialprior.
- **Braunglas ist der Engpass, nicht die Technik.** Braune Behälter werden seltener angefahren (Median 6 statt 9 Messungen, 21,5% der Intervalle > 60 Tage) bei gleichzeitig niedrigem Füllstand (Mittel 36%). Wer Prognosen für Braunglas baut, arbeitet mit der dünnsten Datenbasis und dem niedrigsten Signal.
- **Die Lücken sind überwiegend organisatorisch, nicht sensorisch.** Feiertage sind zu 100% messfrei, Sonntage praktisch auch, und 62,6% der großen Lücken treffen ganze Standorte (alle Materialien gleichzeitig ausgelassen). Das Muster „Messbetrieb an Werktagen, Standort fällt für Monate aus der Tour“ spricht für Tourenplanung/Disposition als Ursache, nicht für defekte Sensorik.
- **Der Häufigkeits-Füllstands-Zusammenhang ist ein Querschnittsartefakt.** Auf Reihenebene korreliert häufigere Messung klar mit höherem Füllstand (+0,41), innerhalb einer Reihe sagt der Füllstand den nächsten Abstand aber nicht voraus (21 Tage in allen Gruppen). Plausibel ist die gemeinsame Ursache „dichte, schnell füllende Stadtlage → mehr Touren *und* höhere Füllstände“; ein bedarfsgesteuertes Nachmessen voller Container lässt sich aus diesen Daten **nicht** belegen.
- **Der Winter ist der blinde Fleck.** Rund 70% aller großen Lücken beginnen zwischen Oktober 2025 und Februar 2026, während Juni/Juli 2026 dicht messen (71,5 bzw. 59,5 Messungen pro Messtag). Eine saisonale Prognose, die auf Winterdaten trainiert wird, steht auf wesentlich weniger Beobachtungen als eine Sommerprognose.

## Grenzen

- Ein Intervall ist nur zwischen zwei Messungen beobachtbar. Ob eine Reihe **am Rand** des Zeitraums ausgefallen ist (vor der ersten oder nach der letzten Messung), bleibt unsichtbar – die Lücken sind nach beiden Seiten zensiert, echte Ausfallzeiten sind also eher unterschätzt.
- Die 34 Reihen mit nur einer Messung (2,5%) sind nicht bewertbar; sie fehlen in der Score-Verteilung.
- Der Score ist eine Setzung: Schwellen 12 Messungen und 180 Tage sowie die 0,30/0,60-Grenzen sind willkürlich, aber transparent. Andere Kappungen verschieben die Klassenanteile um einige Prozentpunkte, nicht die Rangfolge.
- Kalenderbefunde gelten für die geprüften 13 Feiertage in Baden-Württemberg; bewegliche Sonderfälle (Betriebsferien, Brückentage) wurden nicht systematisch geprüft.
- Der Füllstandsvergleich arbeitet mit `overfull` als 110% (tatsächliche Höhe unbekannt) und mit dem Mittel über die gesamte Reihe; ein zeitlicher Trend innerhalb der Reihe ist dabei nicht bereinigt.
- Aggregate über Messtage sind durch die jeweils gemessene Teilmenge verzerrt – an Tagen mit 3 Messungen (z. B. 2025-11-10, 2026-02-18) ist die Stichprobe nicht repräsentativ. Kausalität ist nicht belegt: „Lücke → unsichere Prognose“ ist ein Datenargument, kein Nachweis über die Zuverlässigkeit des Füllstands in der Lücke.

## Nächster Schritt

Die 256 „schlechten“ plus 34 unbewertbaren Reihen als eigene Sperrliste (`prognose_ungeeignet`) aus dem Modelltraining nehmen und vor jedem Prognoselauf die verbleibenden Lücken > 90 Tage im Prognosefenster als explizites Unsicherheitsflag ausweisen.
