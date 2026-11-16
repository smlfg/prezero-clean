# 17 – Leerungszyklen rekonstruieren

> In 708 dicht gemessenen Standort-/Material-Serien lassen sich 1.442 vollständige Füll-/Leerzyklen abgrenzen: Median-Dauer 46 Tage, Median-Zuwachs 50 pp, aber nur 17,9% der Serien mit ≥3 Zyklen füllen sich regelmäßig (CV<0,3).

## Frage

Wie wechseln sich Füllung und Entleerung über die Zeit ab, und wie regelmäßig sind diese Zyklen? Lassen sich Zyklusdauer, Zuwachs und Entleerungstiefe je Material unterscheiden, und hängt die Dauer mit der Füllrate zusammen?

## Vorgehen

- Datengrundlage: `glass_fill_levels_anonymized_f.csv`, `overfull` als 110% kodiert (tatsächliche Höhe unbekannt).
- Filter: nur Standort-/Material-Zeitreihen mit **≥8 Messungen** → 708 Serien, 8.737 Messungen (von 1.338 Serien / 11.701 Zeilen).
- **Zyklus** = Abschnitt zwischen zwei großen negativen Sprüngen: Start = Tiefpunkt (Minimum des Abschnitts), Ende = höchster Wert davor. Ein negativer Sprung ist definiert als Abfall **≥30 pp** zwischen zwei aufeinanderfolgenden Messungen.
- Je Zyklus: Dauer (Tage Tiefpunkt→Peak), Startwert, Peakwert, Zuwachs, Anzahl Messungen, `overfull`-Peak.
- Regelmäßigkeit: Variationskoeffizient (SD/Mittel) der Zyklusdauern je Serie, nur Serien mit ≥3 Zyklen.
- Füllrate = Zuwachs pro Tag, normiert auf pp pro 30 Tage; Zusammenhang per Spearman-Rangkorrelation.
- Segment ohne abschließenden Sprung (letzter Abschnitt jeder Serie) zählt als **offen**, nicht als Zyklus.

## Ergebnisse

**A. Was aus der Datenmenge herauskam**

| Kennzahl | Wert |
|---|---|
| Serien mit ≥8 Messungen | 708 (8.737 Messungen) |
| Serien mit ≥1 vollständigem Zyklus | 669 |
| Serien ohne jeden ≥30-pp-Sprung | 39 (5,5%) |
| Vollständige Zyklen | 1.442 |
| Zyklen je Serie: 1 / 2 / 3+ | 209 / 242 / 218 |
| Verworfene Segmente (1 Messung, kein Anstieg) | 195 |

**B. Zyklusdauer und Zuwachs (alle 1.442 Zyklen)**

| Kennzahl | Q10 | Q1 | Median | Q3 | Q90 | Max |
|---|---|---|---|---|---|---|
| Dauer (Tage) | 19 | 28 | **46** | 86 | 134 | 274 |
| Zuwachs (pp) | 20 | 30 | **50** | 60 | 80 | 110 |
| Messungen im Zyklus | – | 2 | **2** | 4 | – | 10 |

Mittelwert Dauer 63,2 Tage; Mittelwert Zuwachs 48,3 pp. Startwert-Median 50%, Peak-Median 100%. **595 von 1.442 Zyklen (41,3%) enden mit `overfull` (als 110% kodiert).**

**C. Verteilung der Zyklusdauern**

| Dauer | Anteil Zyklen | n | Median-Füllrate (pp/30 d) | Median-Zuwachs |
|---|---|---|---|---|
| ≤30 Tage | 29,5% | 426 | 63,2 | 50 |
| 31–60 Tage | 32,0% | 461 | 31,6 | 40 |
| 61–90 Tage | 15,5% | 224 | 20,4 | 50 |
| 91–180 Tage | 19,8% | 285 | 12,3 | 50 |
| >180 Tage | 3,2% | 46 | 8,1 | 55 |

**D. Zyklusdauer je Material**

| Material | Zyklen | Median Dauer | Q1–Q3 | Median Zuwachs | Start-Median | `overfull`-Peak | Füllrate (pp/30 d) |
|---|---|---|---|---|---|---|---|
| braun | 290 | **65** | 39–107 | 60 | 20% | 19,3% | 25,3 |
| grün | 592 | **41** | 26–76 | 50 | 50% | 34,1% | 30,9 |
| weiß | 560 | **44** | 28–83 | 40 | 60% | 60,2% | 24,7 |

**E. Regelmäßigkeit (Serien mit ≥3 Zyklen, n = 218)**

| Gruppe | Serien | Median CV der Dauer | Anteil CV<0,3 („regelmäßig") |
|---|---|---|---|
| alle | 218 | 0,555 | **17,9%** (39) |
| braun | 37 | 0,531 | 29,7% |
| grün | 95 | 0,583 | 11,6% |
| weiß | 86 | 0,552 | 19,8% |

CV-Quartile: Q1 0,337 · Median 0,555 · Q3 0,823 (Spannweite 0,02–1,35). Bei 451 Serien mit nur 1–2 Zyklen ist Regelmäßigkeit nicht messbar — sie fehlen in dieser Auswertung.

**F. Dauer ↔ Füllrate ↔ Zuwachs**

- Füllrate und Dauer: Spearman **−0,814** auf Zyklusebene, −0,559 auf Serienebene — kurze Zyklen sind schnelle Zyklen, aber es ist teilweise derselbe Bruch (Zuwachs im Nenner).
- Dauer und Zuwachs: Spearman **+0,099** — praktisch kein Zusammenhang. Lange Zyklen entstehen nicht durch größeren Zuwachs, sondern durch langsamere Füllung oder längere Messlücken.
- Leerungstiefe (alle 1.637 Sprünge ≥30 pp): Median 40 pp, Median-Reststand danach 40%; kein Sprung endet bei ≥100%, d. h. jede erkannte Entleerung senkt den Stand wirklich.

## Interpretation

- **Der typische Zyklus ist kurz und grob abgetastet:** Median 46 Tage bei einem typischen Messabstand von ≈41 Tagen heißt, dass ein Zyklus im Median aus **zwei** Messpunkten besteht. Die Zyklusdauer ist damit auf ein Messintervall quantisiert, nicht kontinuierlich gemessen.
- **Kein gleichmäßiger Takt:** Nur knapp ein Fünftel der gut beobachteten Serien leert sich mit stabiler Periode (CV<0,3). Der Median-CV von 0,555 bedeutet, dass die Standardabweichung der Zyklusdauer größer ist als die Hälfte des Mittels — die Leerung folgt eher Bedarf/Ereignis als einem festen Plan.
- **Weiß leert sich am spätesten und am häufigsten zu spät:** 60,2% der weißen Zyklen enden mit `overfull`, bei Braun nur 19,3%. Gleichzeitig ist der Zuwachs bei Weiß am kleinsten (Median 40 pp) und der Startwert am höchsten (60%) — weiße Behälter werden spät geleert und laufen dann über, statt früh mit niedrigem Stand zu starten.
- **Braun hat die längsten Zyklen (65 Tage) und den größten Zuwachs (60 pp)**, startet aber am tiefsten (20%). Das passt zu größerem Behältervolumen oder geringerem Gewicht/Volumen pro Füllgrad, ist mit diesen Daten aber nicht zu beweisen.
- **Füllrate ist der eigentliche Treiber der Dauer**, nicht die Menge: Bei gleichem Zuwachs (Median 50–60 pp) variiert die Dauer um den Faktor 8 zwischen den Dauer-Klassen. Kurze Zyklen (≤30 Tage) laufen mit ~63 pp/30 d, lange (>180 Tage) mit ~8 pp/30 d.
- **Rund 5,5% der dicht gemessenen Serien zeigen nie einen ≥30-pp-Sprung** — sie werden entweder nie geleert, nur teilentleert (<30 pp) oder schwanken ohne klaren Reset. Für diese Standorte ist die Zykluslogik kein brauchbares Planungsmodell.

## Grenzen

- Ein negativer Sprung ist ein **Indiz** für eine Leerung, kein Beleg: Auch Messfehler, Behälterwechsel oder Nachjustierung erzeugen Sprünge. Echte Leerungsereignisse (Datum, Menge, Fahrzeug) fehlen in den Daten.
- Die 30-pp-Schwelle ist eine Setzung. Teilentleerungen unter 30 pp und Doppelleerungen zwischen zwei Messterminen werden nicht erkannt; Zyklen mit nur einer Messung (195 Segmente) fallen ganz heraus.
- **Messauflösung begrenzt die Aussage:** Bei ≈41 Tagen typischem Abstand sind Dauern unter 41 Tagen nur scheinbar präzise; die Quartile 28/86 Tage beruhen auf unterschiedlichen Messrastern der Serien, nicht auf feinerer Beobachtung.
- Nur 708 von 1.338 Serien (53%) haben ≥8 Messungen; die Zyklusstatistik beschreibt also die besser überwachten Standorte, nicht alle 449 Locations. Standorte mit wenigen Messungen (und damit potenziell seltenen Leerungen) sind unterrepräsentiert — der Anteil unregelmäßiger Serien ist dadurch vermutlich **unterschätzt**.
- `overfull` ist als 110% kodiert; die tatsächliche Überschreitung ist unbekannt, „über 100%" also nur ein Ja/Nein-Merkmal.
- `Location_id` ist ein Standort mit mehreren Materialbehältern; ein Zyklus ist kein Nachweis für eine einzelne physische Containerleerung. Koordinaten sind synthetisch und hier nicht verwendet.
- Korrelationen sind keine Kausalität: Füllrate und Dauer teilen sich mathematisch den Zuwachs, die negative Korrelation ist daher teilweise Artefakt der Kennzahl.

## Nächster Schritt

Die 39 Serien ohne jeden ≥30-pp-Sprung (5,5% der dicht gemessenen) einzeln auslesen und klassifizieren — „nie geleert", „nur teilentleert", „Datenfehler" —, weil genau dort die Zyklusannahme bricht und eine route-based-Collection-Planung falsche Prioritäten setzen würde.
