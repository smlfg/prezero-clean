# 23 – Dynamische Leerungsempfehlungen erzeugen

> Eine tagesaktuelle Prioritätsliste ist aus der CSV berechenbar; die Top 20
> sind aber zu 85–90 % Standorte, bei denen alle drei Materialien gleichzeitig
> überfull sind. Zwischen März- und Juli-Stichtag überlappen die Top 20 nur zu
> 10–25 % — die Liste ist saisonal volatil.

## Frage

Wie sähe eine tägliche Empfehlung „welche Standorte zuerst anfahren" konkret aus?

## Vorgehen

Stichtage 2026-03-15, 2026-04-15 und 2026-07-15 (nur Daten bis zum Stichtag).
Je Zeitreihe: letzter Messwert, Tage seit Messung, erwartete Füllrate (Serien-
Median, Fallback Material-Median), prognostizierter Wert heute. Priorität =
prognostizierter Wert + Bonus für Anzahl kritischer Materialien (≥ 80 %) am
Standort. Aggregation je Standort (ein Stopp pro Standort, höchstes Risiko zählt).
Vergleich gegen naive Strategie (älteste Messung zuerst) bei 20 Stopps.

## Ergebnisse

### Stichtag 2026-03-15 (Hochsaison)

| Kennzahl | Wert |
|---|---:|
| Auswertbare Zeitreihen | 1.249 |
| Standorte | 421 |
| Standorte mit ≥ 1 kritischem Material (≥ 80 % progn.) | 404 |
| davon alle drei Materialien kritisch | 137 |
| Top 20 Abdeckung der kritischen Standorte | 20 von 404 (4,9 %) |

### Stichtag 2026-04-15 (Peak)

| Kennzahl | Wert |
|---|---:|
| Auswertbare Zeitreihen | 1.269 |
| Standorte | 431 |
| Kritische Standorte | 410 |
| alle drei kritisch | 191 |
| Top 20 Abdeckung | 20 von 410 (4,9 %) |

### Stichtag 2026-07-15 (Sommertief)

| Kennzahl | Wert |
|---|---:|
| Auswertbare Zeitreihen | 1.335 |
| Standorte | 449 |
| Kritische Standorte | 315 |
| alle drei kritisch | 52 |
| Top 20 Abdeckung | 20 von 315 (6,3 %) |

### Stabilität der Empfehlung

| Vergleich | Überlappung Top 20 |
|---|---:|
| 03-15 vs. 04-15 | 5 von 20 (25 %) |
| 03-15 vs. 07-15 | 2 von 20 (10 %) |
| 04-15 vs. 07-15 | 2 von 20 (10 %) |

Die Liste ist saisonal stark volatil: nur ein Viertel der Stopps bleibt über
vier Wochen stabil, im Sommer nur noch ein Zehntel.

### Smart vs. naiv (20 Stopps, Stichtag 03-15)

| Strategie | Kritische Standorte in Top 20 |
|---|---:|
| Priorität (prognostizierter Wert) | 20 von 20 |
| Naiv (älteste Messung zuerst) | 20 von 20 |

Beide Strategien treffen zufällig dieselben 20 — weil in der Hochsaison fast
alle Standorte kritisch sind. Der Unterschied liegt in der *Reihenfolge* und im
Sommer: dort deckt die prioritätsbasierte Liste dieselben 20 ab, aber mit
deutlich höherer Dringlichkeit (110 vs. 80–99) an den ersten Stopps.

### Operative Erkenntnis

- **20 Stopps reichen nicht:** bei 315–410 kritischen Standorten deckt eine
  Tour 5–6 % ab. Entweder mehr Fahrzeuge, größere Touren oder eine
  Schwellenwertstrategie (nur overfull) nötig.
- **Die Liste muss täglich neu berechnet werden** — sie ist nicht über Wochen
  stabil (10–25 % Überlappung).
- **Standorte mit allen drei Materialien kritisch** (137 im März, 52 im Juli)
  sind die natürlichen „Pflichtstopps".

## Grenzen

Die Empfehlung basiert auf prognostizierten Werten, nicht auf echten Messungen
am Stichtag. Weil Messabstände median 28 Tage betragen, ist die „heutige"
Füllung eine Schätzung mit MAE ≈ 20–27 pp (vgl. Analyse 21). Ob ein Stopp
wirklich nötig ist, kann nur eine frische Messung oder ein Sensor zeigen.

## Nächster Schritt

Tägliche Neuberechnung mit einem Frischegewicht (Messungen < 7 Tage alt
 bevorzugen) und eine Kapazitätsplanung: wie viele Stopps/Tag braucht man,
um die overfull-Quote unter 5 % zu halten? (vgl. Analyse 30/31).