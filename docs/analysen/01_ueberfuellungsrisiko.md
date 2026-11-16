# 01 – Überfüllungsrisiken erkennen

> 44,7 % aller 11.701 Messungen liegen bei ≥ 80 %, 10,2 % sind overfull (als 110 % kodiert, tatsächliche Höhe unbekannt) – das Risiko ballt sich in weißen Behältern (66,4 % ≥ 80 %) und in den fünf Monaten Januar bis Mai 2026 (74,9 % aller overfull-Messungen).

## Frage

Welche Container und Standorte werden besonders häufig kritisch, wie verteilt sich das Risiko
über Materialien, Standorte und Monate – und welche Zeitreihen führen?

## Vorgehen

- Datengrundlage: `glass_fill_levels_anonymized_f.csv`, 11.701 Messungen, 449 `Location_id`,
  1.338 Standort-Material-Zeitreihen, 2025-10-17 bis 2026-09-30, 229 Messtage.
- Risikokennzahl: Messung ≥ 80 % (80, 90, 100, overfull); `overfull` = 110 % in Rechnungen.
  Score = 2 × overfull-Anteil + Anteil 80–100 % (0–2), overfull doppelt gewichtet.
- Filter Mindestmessungen: Zeitreihen ≥ 8 (Median der Verteilung), Standorte ≥ 10. Monat =
  Kalendermonat des Messdatums. Alle Werte direkt aus der CSV berechnet.

## Ergebnisse

### Je Material

| Material | Messungen | overfull | overfull-Anteil | ≥ 80 % | ≥ 80-Anteil | Ø Füllstand |
|---|---:|---:|---:|---:|---:|---:|
| white | 4.432 | 731 | 16,5 % | 2.945 | 66,4 % | 82,2 % |
| green | 4.169 | 357 | 8,6 % | 1.825 | 43,8 % | 68,1 % |
| brown | 3.100 | 104 | 3,4 % | 457 | 14,7 % | 40,0 % |
| **Gesamt** | **11.701** | **1.192** | **10,2 %** | **5.227** | **44,7 %** | **66,0 %** |

Davon 4.035 Messungen (34,5 %) im Bereich 80–100 %. Weiß stellt 37,9 % der Messungen, aber
61,3 % aller overfull-Messungen; Grün 29,9 %, Braun 8,7 %.

### Je Monat

| Monat | Messungen | overfull | overfull-Anteil | ≥ 80 % | ≥ 80-Anteil | Ø Füllstand |
|---|---:|---:|---:|---:|---:|---:|
| 2025-10 | 741 | 3 | 0,4 % | 212 | 28,6 % | 55,6 % |
| 2025-11 | 656 | 14 | 2,1 % | 253 | 38,6 % | 59,5 % |
| 2025-12 | 1.357 | 14 | 1,0 % | 594 | 43,8 % | 62,9 % |
| 2026-01 | 783 | 91 | 11,6 % | 469 | 59,9 % | 76,1 % |
| 2026-02 | 657 | 85 | 12,9 % | 386 | 58,8 % | 76,5 % |
| 2026-03 | 776 | 292 | 37,6 % | 530 | 68,3 % | 85,2 % |
| 2026-04 | 896 | 209 | 23,3 % | 606 | 67,6 % | 82,3 % |
| 2026-05 | 951 | 216 | 22,7 % | 519 | 54,6 % | 74,4 % |
| 2026-06 | 1.501 | 78 | 5,2 % | 371 | 24,7 % | 53,7 % |
| 2026-07 | 1.310 | 65 | 5,0 % | 514 | 39,2 % | 61,4 % |
| 2026-08 | 1.215 | 34 | 2,8 % | 407 | 33,5 % | 57,5 % |
| 2026-09 | 858 | 91 | 10,6 % | 366 | 42,7 % | 64,1 % |

Januar bis Mai 2026 umfassen 34,7 % aller Messungen, aber 74,9 % aller overfull-Messungen;
allein der März 2026 enthält 24,5 % aller overfull-Messungen.

### Top-20 Risiko-Zeitreihen (≥ 8 Messungen, 708 Zeitreihen)

| # | Standort | Material | Mess. | overfull | ≥ 80 % | overfull-Anteil | ≥ 80-Anteil | Ø Füllstand | Score |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `da3a78d0` | white | 16 | 8 | 16 | 50,0 % | 100,0 % | 102 % | 1,50 |
| 2 | `0408b512` | white | 11 | 5 | 10 | 45,5 % | 90,9 % | 95 % | 1,36 |
| 3 | `1a342cc5` | white | 9 | 4 | 8 | 44,4 % | 88,9 % | 97 % | 1,33 |
| 4 | `83086ae1` | white | 16 | 5 | 16 | 31,2 % | 100,0 % | 99 % | 1,31 |
| 5 | `de821fab` | white | 8 | 3 | 7 | 37,5 % | 87,5 % | 94 % | 1,25 |
| 6 | `05e819c6` | white | 12 | 4 | 11 | 33,3 % | 91,7 % | 97 % | 1,25 |
| 7 | `c347d4ef` | white | 8 | 2 | 8 | 25,0 % | 100,0 % | 90 % | 1,25 |
| 8 | `eecbf6fa` | white | 29 | 12 | 24 | 41,4 % | 82,8 % | 91 % | 1,24 |
| 9 | `80b7f22a` | green | 17 | 9 | 12 | 52,9 % | 70,6 % | 88 % | 1,24 |
| 10 | `df03fc92` | white | 17 | 7 | 14 | 41,2 % | 82,4 % | 93 % | 1,24 |
| 11 | `5121497c` | white | 18 | 6 | 16 | 33,3 % | 88,9 % | 97 % | 1,22 |
| 12 | `c7208f1a` | white | 18 | 6 | 16 | 33,3 % | 88,9 % | 96 % | 1,22 |
| 13 | `6585283f` | white | 9 | 3 | 8 | 33,3 % | 88,9 % | 98 % | 1,22 |
| 14 | `148e5bd5` | white | 15 | 3 | 15 | 20,0 % | 100,0 % | 97 % | 1,20 |
| 15 | `e5466d8a` | white | 20 | 7 | 17 | 35,0 % | 85,0 % | 94 % | 1,20 |
| 16 | `815e06ce` | white | 15 | 5 | 13 | 33,3 % | 86,7 % | 97 % | 1,20 |
| 17 | `df6d6307` | green | 15 | 5 | 13 | 33,3 % | 86,7 % | 95 % | 1,20 |
| 18 | `4776173b` | white | 11 | 2 | 11 | 18,2 % | 100,0 % | 95 % | 1,18 |
| 19 | `38ff2db8` | white | 11 | 5 | 8 | 45,5 % | 72,7 % | 89 % | 1,18 |
| 20 | `80b7f22a` | white | 17 | 6 | 14 | 35,3 % | 82,4 % | 92 % | 1,18 |

18 der 20 Spitzenreihen sind weiß, 2 grün. 17 der 708 Zeitreihen erreichen Score ≥ 1,2, 104
einen Score ≥ 1,0 (Median 0,60); 77 liegen bei overfull-Anteil ≥ 25 %, 40 (5,6 %) erreichen
nie 80 %.

### Top-20 Risiko-Standorte (≥ 10 Messungen, 408 Standorte)

| # | Standort | Mess. | overfull | ≥ 80 % | overfull-Anteil | ≥ 80-Anteil | Ø Füllstand | Score |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `7d069a27` | 12 | 5 | 9 | 41,7 % | 75,0 % | 82 % | 1,17 |
| 2 | `80b7f22a` | 43 | 18 | 30 | 41,9 % | 69,8 % | 87 % | 1,12 |
| 3 | `83086ae1` | 40 | 9 | 32 | 22,5 % | 80,0 % | 88 % | 1,02 |
| 4 | `d5be6df1` | 35 | 7 | 28 | 20,0 % | 80,0 % | 92 % | 1,00 |
| 5 | `df6d6307` | 42 | 10 | 30 | 23,8 % | 71,4 % | 84 % | 0,95 |
| 6 | `5f14179e` | 39 | 10 | 27 | 25,6 % | 69,2 % | 83 % | 0,95 |
| 7 | `1a342cc5` | 19 | 6 | 11 | 31,6 % | 57,9 % | 80 % | 0,89 |
| 8 | `94bc9aca` | 34 | 7 | 23 | 20,6 % | 67,6 % | 85 % | 0,88 |
| 9 | `00e9e2cf` | 48 | 9 | 33 | 18,8 % | 68,8 % | 81 % | 0,88 |
| 10 | `da3a78d0` | 46 | 10 | 30 | 21,7 % | 65,2 % | 79 % | 0,87 |
| 11 | `c7208f1a` | 45 | 9 | 30 | 20,0 % | 66,7 % | 82 % | 0,87 |
| 12 | `387a24ec` | 40 | 7 | 27 | 17,5 % | 67,5 % | 78 % | 0,85 |
| 13 | `df03fc92` | 46 | 10 | 29 | 21,7 % | 63,0 % | 79 % | 0,85 |
| 14 | `6fcbb4bd` | 13 | 2 | 9 | 15,4 % | 69,2 % | 78 % | 0,85 |
| 15 | `9dc40dd4` | 47 | 11 | 28 | 23,4 % | 59,6 % | 72 % | 0,83 |
| 16 | `a6e674b2` | 47 | 10 | 29 | 21,3 % | 61,7 % | 78 % | 0,83 |
| 17 | `d9a4e9d2` | 23 | 4 | 15 | 17,4 % | 65,2 % | 82 % | 0,83 |
| 18 | `eecbf6fa` | 80 | 21 | 45 | 26,2 % | 56,2 % | 76 % | 0,82 |
| 19 | `0408b512` | 28 | 6 | 17 | 21,4 % | 60,7 % | 78 % | 0,82 |
| 20 | `f019215f` | 11 | 3 | 6 | 27,3 % | 54,5 % | 83 % | 0,82 |

Die Top-20-Standorte vereinen 6,3 % der Messungen, aber nur 14,6 % der overfull-Messungen;
113 der 449 Standorte haben keine overfull-Messung, der Median-Standort 8,0 % overfull-Anteil.
**Nie 80 % erreichen 10 von 449 Standorten (2,2 %)**, bei Filter ≥ 10 nur einer (`bf290a6e`,
12 Mess., Ø 45,8 %); ferner `1e25f5f5` (9/43,3 %), `43ff3a23` (9/36,7 %), `79d39648` (9/34,4 %),
`93bf97b0` (9/46,7 %), `4e2ca848` (4/30,0 %), `e3b71c5d` (4/50,0 %), `fbe1b4ea` (4/37,5 %),
`53a56d2e` (2/40,0 %), `b13d8ab0` (2/25,0 %).

## Interpretation

- **Weiß ist der Treiber.** 18 der 20 Spitzenreihen sind weiß, weil sie im Mittel ohnehin bei
  82,2 % liegen: ein weißer Behälter mit 80 % ist fast Normalzustand, nicht Ausnahme.
- **Das Risiko ist breit verteilt, nicht punktuell.** Die 20 schlechtesten Standorte tragen
  14,6 % der overfull-Messungen bei 6,3 % der Messungen (Faktor 2,3).
- **Standort `80b7f22a` ist der auffälligste Fall.** Grün Platz 9, Weiß Platz 20 der Zeitreihen,
  Standort Platz 2 (43 Messungen, 18 overfull) – ein Problem des ganzen Standorts.
- **Der März 2026 ist ein Ausnahmemonat.** 37,6 % overfull, Ø 85,2 %, aber nur 86 braune und
  422 weiße Messungen – ein Teil des Ausschlags ist Messaufkommen, nicht Füllverhalten.

## Grenzen

- **Keine Leerungsereignisse, kategoriale Skala.** „Nicht geleert“ und „viel Verkehr“ sind
  nicht unterscheidbar (negative Sprünge nur Indizien); overfull = 110 %, 150 % zählt wie 105 %.
- **Monatsvergleiche verzerrt, Abstände unregelmäßig.** Pro Monat wurden unterschiedliche
  Teilmengen gemessen (braun: 86 im März, 449 im Dezember); Median-Abstand etwa 41 Tage,
  Minimum 1 Messung je Zeitreihe – der Filter ≥ 8 reduziert das, beseitigt es nicht.
- **`Location_id` ist ein Standort, kein Container**, dahinter stehen ggf. mehrere Behälter je
  Material; der Score ist eine Setzung, andere Gewichtung verschiebt die Reihenfolge. 100 %
  sagt zudem nichts über Liter oder Anwohner; die Koordinaten sind synthetisch, keine Adressen.

## Nächster Schritt

Für die Top-20-Standorte Leerungszeitstempel (Datum, Material, Fahrzeug) nachziehen und je
Messung prüfen, ob dazwischen geleert wurde – erst das trennt Überlauf von hoher Auslastung.
