# 21 – Prognosemodell für Füllstände bauen

> Die beste einfache Methode ist der Material-Median (MAE 21,0 pp, Trefferquote
> ±20 pp 66,3 %); Persistence (MAE 25,4) und ein Drift-Modell (MAE 27,5) sind
> schlechter. scikit-learn ist nicht installiert, ein Ridge-Modell konnte nicht
> trainiert werden.

## Frage

Wie gut lässt sich der nächste Füllstand einer Zeitreihe aus der Historie
vorhersagen?

## Vorgehen

Zeitlicher Split: pro Zeitreihe die letzten 20 % der Messungen als Test (kein
Zufallssplit, um Leckagen zu vermeiden). Drei Baselines auf derselben Testmenge
(n = 2.712 Übergänge): (1) Persistence (letzter Wert), (2) Material-Median,
(3) Drift (letzter Wert + Serien-Median-Rate × Tage, Fallback Material-Median).
Metriken: MAE, RMSE, Median-AE, Trefferquote ±20 pp. Auswertung zusätzlich je
Material und je Messabstand.

## Ergebnisse

### Gesamtvergleich (Testmenge, n = 2.712)

| Modell | MAE (pp) | RMSE (pp) | Median-AE (pp) | ±20 pp |
|---|---:|---:|---:|---:|
| Material-Median | 21,00 | 26,82 | 20,00 | 66,3 % |
| Persistence | 25,36 | 33,74 | 20,00 | 59,4 % |
| Drift (Rate × Tage) | 27,47 | 36,04 | 20,00 | 51,6 % |

Der Material-Median gewinnt, obwohl er die Historie ignoriert — das zeigt, wie
schwach der zeitliche Zusammenhang ist. Drift ist das schlechteste Modell, weil
die Rate aus spärlichen, unregelmäßigen Messungen (Median 28 Tage Abstand)
stark verrauscht ist.

### Je Material (Drift-Modell, MAE in pp)

| Material | n Test | MAE |
|---|---:|---:|
| brown | 719 | 24,47 |
| green | 965 | 29,37 |
| white | 1.028 | 27,77 |

Braunglas ist am besten vorhersagbar (niedrigste Varianz), Weißglas am
schlechtesten (höchste Auslastung + overfull-Rauschen).

### Je Messabstand (Drift-Modell, MAE in pp)

| Abstand | n Test | MAE |
|---|---:|---:|
| < 30 Tage | 1.547 | 24,77 |
| 30–60 Tage | 981 | 29,62 |
| > 60 Tage | 184 | 38,69 |

Mit wachsendem Abstand bricht die Vorhersage ein. Für Prognosen > 60 Tage ist
kein Modell aus dieser CSV zuverlässig.

### Warum kein besseres Modell?

- **Zielgröße ist kategorial** (Vielfache von 10, plus overfull) — MAE und RMSE
  sind deshalb grob; ein Klassifikator wäre ehrlicher, aber die Klassen sind
  unbalanciert.
- **Datenmenge pro Zeitreihe ist klein** (Median 8 Messungen, min 1) — kein
  Zeitreihenmodell (ARIMA, exponentielles Glätten) kann robust geschätzt werden.
- **scikit-learn ist nicht installiert** — ein Ridge-Modell mit Features
  (letzter Wert, Tage seit letzter Messung, Material-One-Hot, Monat Sin/Cos,
  Zeitreihen-Mittel) konnte nicht trainiert werden. Das ist ein Infrastruktur-
  Befund, kein methodischer: mit sklearn wäre ein Vergleich möglich, die
  erwartete Verbesserung ist aber angesichts der Datenlage gering.
- **Leckage-Risiko:** ein Zufallssplit würde die Werte aufblähen; der zeitliche
  Split ist konservativ und ehrlich.

## Grenzen

Das Modell prognostiziert die *nächste Messung*, nicht den Füllstand an einem
beliebigen künftigen Tag. Weil Messabstände unregelmäßig sind (Median 28 Tage),
ist „nächste Messung" keine feste Horizontlänge. Ein echtes Prognosemodell für
Tourenplanung braucht tägliche Beobachtungen oder explizite Leerungsereignisse.

## Nächster Schritt

Für den Prototypen den Material-Median als Baseline (null-Modell) einführen und
alle weiteren Modelle dagegen messen; gleichzeitig Messfrequenz auf tägliche
Werte oder Leerungsereignisse anheben, sonst bleibt jede Prognose bei MAE ≈ 20 pp.