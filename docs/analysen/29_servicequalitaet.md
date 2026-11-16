# 29 – Servicequalität messen

> Kennzahlen für die Qualität der Leerungsplanung: 44,7 % der Messungen ≥ 80 %,
> 10,2 % overfull, Mittelwert 66,0 %. Im März 2026 sind 37,6 % der Messungen
> overfull — im Juni nur 5,2 %. Die Servicequalität schwankt saisonal um den
> Faktor 7.

## Frage

Welche Kennzahlen eignen sich, um die Qualität der Leerungsplanung zu messen?

## Vorgehen

Definition und Berechnung eines Kennzahlen-Sets aus der CSV: Überfüllungsquote,
Anteil kritischer Messungen (≥ 80 %), mittlerer Füllstand, Anteil Standorte mit
mindestens einer overfull-Messung. Darstellung gesamt, je Material und je Monat.
Zusätzlich: Vorschlag einer zusammengesetzten Service-Score-Formel.

## Ergebnisse

### Kennzahlen gesamt (11.701 Messungen)

| Kennzahl | Wert |
|---|---:|
| Mittlerer Füllstand | 66,0 % |
| Anteil Messungen ≥ 80 % | 44,7 % |
| Anteil Messungen ≥ 90 % | 35,2 % |
| Anteil overfull | 10,2 % |
| Standorte mit ≥ 1 overfull-Messung | 336 von 449 (74,8 %) |

### Je Material

| Material | Mittelwert | ≥ 80 % | overfull |
|---|---:|---:|---:|
| brown | 40,0 % | 14,7 % | 3,4 % |
| green | 68,1 % | 43,8 % | 8,6 % |
| white | 82,2 % | 66,4 % | 16,5 % |

### Monatliche Servicequalität

| Monat | Messungen | Mittelwert | ≥ 80 % | overfull |
|---|---:|---:|---:|---:|
| 2025-10 | 741 | 55,6 % | 28,6 % | 0,4 % |
| 2025-11 | 656 | 59,5 % | 38,6 % | 2,1 % |
| 2025-12 | 1.357 | 62,9 % | 43,8 % | 1,0 % |
| 2026-01 | 783 | 76,1 % | 59,9 % | 11,6 % |
| 2026-02 | 755 | 76,5 % | 58,8 % | 12,9 % |
| 2026-03 | 776 | 85,2 % | 68,3 % | 37,6 % |
| 2026-04 | 896 | 82,3 % | 67,6 % | 23,3 % |
| 2026-05 | 951 | 74,4 % | 54,6 % | 22,7 % |
| 2026-06 | 1.501 | 53,7 % | 24,7 % | 5,2 % |
| 2026-07 | 1.310 | 61,4 % | 39,2 % | 5,0 % |
| 2026-08 | 1.215 | 57,5 % | 33,5 % | 2,8 % |
| 2026-09 | 858 | 64,1 % | 42,7 % | 10,6 % |

### Vorschlag: zusammengesetzter Service-Score

```
Service-Score = 100 − (overfull-Rate × 2 + kritische-Rate × 0,5)
```

mit overfull-Rate und kritischer Rate in Prozent. Ergebnis 0–100, höher ist
besser. Auf Gesamtdaten: 100 − (10,2 × 2 + 44,7 × 0,5) = **64,4**.
Zielwert für einen guten Monat (z. B. Juni): 100 − (5,2 × 2 + 24,7 × 0,5) =
**84,9**. Zielwert für einen schlechten Monat (März): 100 − (37,6 × 2 + 68,3 × 0,5) =
**−6,7** (bzw. 0 nach Clipping).

### Vergleichbarkeit

Die Kennzahlen sind nur vergleichbar, wenn dieselbe Messmethode und derselbe
Zeitraum verwendet werden. Weil die Messabdeckung ungleichmäßig ist (Analyse 20),
sollten die Kennzahlen standortgleich gewichtet werden (63,7 % statt 66,0 %).

## Grenzen

Die Kennzahlen messen den *Zustand*, nicht die *Ursache*. Eine hohe
Überfüllungsquote kann durch zu kleine Behälter, zu seltene Leerung, Messfehler
oder saisonale Spitzen entstehen — die CSV trennt diese nicht. Der
Service-Score ist ein Vorschlag, keine normierte Kennzahl.

## Nächster Schritt

Kennzahlen als Dashboard (Analyse 34) implementieren und monatlich tracken;
Zielwerte (z. B. overfull-Rate < 5 %) mit dem Mentor abstimmen, sobald
echte Leerungsdaten vorliegen.