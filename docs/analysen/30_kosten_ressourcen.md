# 30 – Kosten und Ressourcen planen

> An einem durchschnittlichen Messtag sind 13 Standorte kritisch (Median),
> in der Spitze 40. Das sind die Anfahrten, die eine bedarfsgesteuerte Planung
> priorisieren würde — gegenüber einem festen Turnus, der auch bei 1 kritischem
> Standort die ganze Tour fährt.

## Frage

Wie lassen sich aus Prioritäten und erwarteten Leerungen Personal-, Fahrzeug-
und Zeitbedarf besser abschätzen?

## Vorgehen

Schätzung der täglichen Leerungsanforderung aus der CSV: Anzahl kritischer
Standorte pro Messtag (≥ 80 %), je Material. Vergleich mit einem festen
Turnus (alle Standorte). Abschätzung der Einsparung als Differenz. Keine
Kostenrechnung in Euro — nur Mengengerüste.

## Ergebnisse

### Kritische Stopps pro Messtag (229 Messtage)

| Kennzahl | Wert |
|---|---:|
| Median kritische Standorte/Tag | 13 |
| Mittelwert | 13,7 |
| Minimum | 1 |
| Maximum | 40 |
| Summe über alle Messtage | 3.115 |

### Je Material (Median kritische Stopps/Tag)

| Material | Median/Tag | Maximum/Tag |
|---|---:|---:|
| brown | 2 | 24 |
| green | 7 | 30 |
| white | 13 | 38 |

Weiße Glasbehälter dominieren den Tagesbedarf: 13 von 13,7 kritischen Stopps
sind Weißglas-Standorte.

### Vergleich: bedarfsgesteuert vs. fester Turnus

| Strategie | Stopps/Tag (Median) | Annahme |
|---|---:|---|
| Bedarfsgesteuert (nur ≥ 80 %) | 13 | nur kritische Standorte anfahren |
| Fester Turnus (alle 449 Standorte) | 449 / Intervall | z. B. 1/4 der Standorte pro Tag ≈ 112 Stopps |
| Einsparung (Median) | ≈ 99 Stopps/Tag | bei 4-Tage-Turnus |

Eine bedarfsgesteuerte Tour könnte rund 90 % der Stopps einsparen — **wenn**
die Messwerte frisch genug sind. Bei median 28 Tagen Messabstand (Analyse 18)
ist das nicht der Fall: viele „kritische" Standorte sind es längst nicht mehr.

### Ressourcenabschätzung (Mengengerüst, keine Kosten)

| Größe | Schätzung | Basis |
|---|---|---|
| Stopps/Tag (bedarfsgesteuert) | 13 (Median), 40 (Spitze) | CSV, ≥ 80 % |
| Fahrzeuge nötig bei 20 Stopps/Fahrzeug | 1 (Median), 2 (Spitze) | Annahme 20 Stopps/Fahrzeug |
| Servicezeit/Tag | 65–200 min | Annahme 5 min/Stopp |
| Fahrstrecke | unbekannt | keine echten Koordinaten |

### Saisonale Schwankung des Ressourcenbedarfs

| Periode | Kritische Stopps/Tag (Median) |
|---|---:|
| März–April (Peak) | ≈ 25–30 |
| Juni–August (Tief) | ≈ 5–8 |
| Oktober–November | ≈ 8–12 |

Der Bedarf schwankt um den Faktor 4–5 — ein fixes Fuhrpark- und
Personalbudget ist entweder in der Hochsaison zu klein oder im Sommer zu groß.

## Grenzen

Alle Zahlen sind Messwert-basiert, nicht Leerungs-basiert. Die 13 kritischen
Stopps/Tag sind eine Untergrenze (Messungen fehlen an Feiertagen, Analyse 18)
und gleichzeitig eine Überschätzung (viele Messungen sind veraltet). Ohne
echte Leerungsdaten, Fahrzeugkapazitäten und Servicezeiten ist keine
Kostenrechnung möglich — die Mengengerüste sind Planungsgrößen, keine
Budgets.

## Nächster Schritt

Mengengerüst mit dem Mentor abgleichen und in eine Kapazitätsplanung
überführen: wie viele Fahrzeuge/Stopps braucht man in der Peak-Woche (März)
vs. der Tief-Woche (Juni), und welche Flexibilität (Leihfahrzeuge, Springer)
ist sinnvoll?