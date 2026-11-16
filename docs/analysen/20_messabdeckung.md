# 20 – Messabdeckung bewerten

> 449 Standorte, Median 24 Messungen je Standort (10.–90. Perzentil 10–45); der
> ungewichtete Gesamtmittelwert (66,0 %) liegt 2,3 pp über dem standortgleich
> gewichteten (63,7 %) — Vielmessung korreliert mit höherem Füllstand (r = 0,39).

## Frage

Welche Standorte werden häufig, welche nur selten gemessen — und verzerrt das die
Gesamtbilder?

## Vorgehen

Aggregation je `Location_id`: Anzahl Messungen, Messtage, Zeitspanne, Materialien,
längste Lücke. Vergleich dreier Mittelwerte (ungewichtet / standortgleich /
nur ≥ 8 Messungen). Korrelation Messhäufigkeit vs. Standortmittel, Kreuztabelle
Material × Messhäufigkeitsklasse.

## Ergebnisse

### Verteilung der Messhäufigkeit (449 Standorte)

| Kennzahl | Wert |
|---|---:|
| Minimum | 1 |
| 10. Perzentil | 10 |
| 25. Perzentil | 16 |
| Median | 24 |
| 75. Perzentil | 35 |
| 90. Perzentil | 45 |
| Maximum | 97 |
| Mittelwert | 26,1 |
| Standorte mit ≥ 8 Messungen | 424 (94,4 %) |
| Standorte mit < 5 Messungen | 12 (2,7 %) |
| Standorte mit 1 Messung | 1 |
| Messtage je Standort (Median) | 9 (Max 37) |

### Drei Mittelwerte — wie stark verzerrt die Abdeckung?

| Mittelung | Wert | n |
|---|---:|---:|
| Ungewichtet über Messungen | 66,0 % | 11.701 |
| Standortgleich (je Standort ein Wert) | 63,7 % | 449 |
| Nur Standorte mit ≥ 8 Messungen (standortgleich) | 63,9 % | 424 |

Differenz ungewichtet vs. standortgleich: **+2,3 pp**. Die Verzerrung ist klein,
aber systematisch: Standorte mit mehr Messungen sind voller.

### Korrelation Messhäufigkeit vs. Standortmittel

- Pearson r(n, Standortmittel) = **0,391** (n = 449).
- Top-5 Standorte (75–97 Messungen) liegen im Mittel bei 71–84 %.
- Bottom-5 (1–3 Messungen) liegen bei 20–55 %.

### Material × Messhäufigkeit

| Material | Messungen je Standort (Median) | min–max |
|---|---:|---:|
| brown | 6 | 0–26 |
| green | 9 | 0–35 |
| white | 9 | 0–37 |

Braunglas-Standorte werden seltener gemessen (Median 6 statt 9). Weil Braun
gleichzeitig die niedrigste Auslastung hat, entsteht ein Teil der Verzerrung
über das Material, nicht über die Standortwahl.

### Monatliche Abdeckung

| Monat | Messungen | Standorte mit ≥ 1 Messung |
|---|---:|---:|
| 2025-10 | 741 | — |
| 2025-11 | 656 | — |
| 2025-12 | 1.357 | — |
| 2026-01 | 783 | — |
| 2026-02 | 755 | — |
| 2026-03 | 1.501 | — |
| 2026-04 | 1.149 | — |
| 2026-05 | 1.143 | — |
| 2026-06 | 1.026 | — |
| 2026-07 | 699 | — |
| 2026-08 | 736 | — |
| 2026-09 | 755 | — |

Die Monatsmittel sind durch die jeweils gemessene Teilmenge beeinflusst — ein
Monat mit vielen Messungen enthält mehr Daten, aber nicht notwendigerweise mehr
Standorte.

### Extremfälle

- **Top-5 häufig gemessen:** 97, 91, 80, 79, 75 Messungen (Mittelwerte 71–84 %).
- **Bottom-5:** 1, 2, 2, 2, 3 Messungen (Mittelwerte 20–55 %).
- **Längste Zeitspanne** eines Standorts: 347 Tage; Median 307 Tage.

### Welche Kennzahlen sind vorsichtig zu lesen?

1. **Tages- und Monatsmittel** — sie sind Mittel der gemessenen Teilmenge, nicht
   des Gesamtbestands.
2. **Überfüllungsquote** — sie hängt von der Messhäufigkeit ab: häufig gemessene
   (und vollere) Standorte erzeugen mehr overfull-Messungen.
3. **Standort-Rankings** — bei < 8 Messungen sind Ränge nicht stabil (vgl.
   Analyse 08: Rangkorrelation zwischen Halbjahren nur 0,30).

## Grenzen

Die Abdeckung ist eine Eigenschaft der Erhebung, nicht des Systems. Ob die
Messungen zufällig, bedarfsgesteuert (volle Container häufiger) oder nach einem
festen Plan erfolgten, ist aus der CSV nicht rekonstruierbar. Die 2,3-pp-Differenz
ist ein Untergrenze: wenn Messungen gezielt an vollen Standorten stattfanden,
ist die wahre mittlere Auslastung niedriger als 63,7 %.

## Nächster Schritt

Messprotokoll und Auswahlregel der Standorte beim PreZero-Mentor erfragen; im
Prototypen Messabdeckung als Metadatenfeld (n Messungen, letzter Messtag) pro
Standort ausweisen, damit Kennzahlen mit geringer Basis als „niedrige Evidenz"
markiert werden können.