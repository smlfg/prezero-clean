# 22 – Überlaufwahrscheinlichkeit prognostizieren

> Einfaches bucket-basiertes Modell schlägt die Basisrate: Brier 0,196 vs. 0,249
> für ≥ 80 %. Die Wahrscheinlichkeit hängt stark vom Material ab — bei gleichem
> aktuellen Wert ist Weißglas 2–5× wahrscheinlicher kritisch als Braunglas.

## Frage

Mit welcher Wahrscheinlichkeit erreicht eine Zeitreihe bei der nächsten Messung
≥ 80 %, 100 % oder `overfull`?

## Vorgehen

Empirische Wahrscheinlichkeiten statt Blackbox: für jede Beobachtung werden
aktueller Wert (5 Klassen: 0–39, 40–59, 60–79, 80–99, overfull) und Material
mit dem Label (nächster Wert ≥ Schwelle) verknüpft. Kalibrierung mit zeitlichem
Split (letzte 20 % je Zeitreihe als Test). Brier-Score gegen Basisrate.

## Ergebnisse

### P(nächste Messung ≥ 80 %) nach aktuellem Wert und Material

| aktueller Wert | braun | grün | weiß | n (gesamt) |
|---|---:|---:|---:|---:|
| 0–39 % | 0,109 | 0,301 | 0,555 | 2.207 |
| 40–59 % | 0,193 | 0,365 | 0,609 | 1.637 |
| 60–79 % | 0,212 | 0,422 | 0,626 | 1.754 |
| 80–99 % | 0,296 | 0,546 | 0,709 | 3.674 |
| overfull | 0,341 | 0,512 | 0,672 | 1.091 |

### P(nächste Messung ≥ 100 %)

| aktueller Wert | braun | grün | weiß |
|---|---:|---:|---:|
| 0–39 % | 0,057 | 0,162 | 0,376 |
| 40–59 % | 0,092 | 0,196 | 0,389 |
| 60–79 % | 0,106 | 0,258 | 0,378 |
| 80–99 % | 0,182 | 0,319 | 0,456 |
| overfull | 0,187 | 0,306 | 0,453 |

### P(nächste Messung overfull)

| aktueller Wert | braun | grün | weiß |
|---|---:|---:|---:|
| 0–39 % | 0,026 | 0,043 | 0,139 |
| 40–59 % | 0,046 | 0,060 | 0,149 |
| 60–79 % | 0,057 | 0,107 | 0,125 |
| 80–99 % | 0,056 | 0,112 | 0,187 |
| overfull | 0,066 | 0,151 | 0,234 |

### Kalibrierung (zeitlicher Split, n Test = 2.712)

| Schwelle | Brier (Modell) | Brier (Basisrate) | Basisrate |
|---|---:|---:|---:|
| ≥ 80 % | 0,196 | 0,249 | 0,460 |
| ≥ 100 % | 0,161 | 0,179 | 0,281 |
| overfull | 0,060 | 0,061 | 0,112 |

Das Modell schlägt die Basisrate bei ≥ 80 % und ≥ 100 % deutlich; bei overfull
ist der Gewinn marginal, weil overfull selten ist und die Klassen sehr unbalanciert.

### Nutzungstabelle (Auszug)

| Heute | Material | P(≥ 80 % nächste Messung) |
|---|---|---:|
| 0–39 % | braun | 10,9 % |
| 0–39 % | weiß | 55,5 % |
| 80–99 % | braun | 29,6 % |
| 80–99 % | weiß | 70,9 % |
| overfull | weiß | 67,2 % |

## Grenzen

- Die „nächste Messung" ist keine feste Zeit (Median-Abstand 28 Tage) — die
  Wahrscheinlichkeit sagt nichts über die Tage bis zum Überlauf aus (dafür
  Analyse 05).
- Mit nur einem Jahr Daten sind saisonale Effekte nicht aus der bedingten
  Wahrscheinlichkeit herausgerechnet; ein weißer Container im März hat eine
  höhere reale Überlaufwahrscheinlichkeit als im Juni.
- Die Tabelle ist eine Häufigkeitsaussage, keine kausale: ein Container, der
  heute overfull ist, wird oft schon vor der nächsten Messung geleert — die 67 %
  messen also das Systemverhalten, nicht den reinen Füllprozess.

## Nächster Schritt

Die Tabelle als Lookup in den Scoring-Schritt (02/05) einbauen und mit einem
zeitlichen Holdout regelmäßig neu kalibrieren; sobald Leerungsereignisse
vorliegen, das Modell auf „Zeit bis Leerung" umstellen.