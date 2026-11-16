# 31 – Einsparpotenziale finden

> Nur 9 von 449 Standorten (2,0 %) waren in der gesamten Beobachtungszeit
> nie kritisch (Mittelwert < 50 % und Maximum < 80 %). Die Daten zeigen also
> kaum dauerhaft leere Container — Einsparungen kommen vor allem aus der
> Bündelung von selten kritischen Standorten und aus saisonaler Drosselung.

## Frage

Wo lassen sich Leerungen bündeln oder Intervalle verlängern, ohne stark
ausgelastete Standorte zu vernachlässigen?

## Vorgehen

Identifikation dauerhaft niedrig ausgelasteter Standorte (Mittelwert < 50 %
und nie ≥ 80 %). Materialverteilung dieser Gruppe. Saisonale Einsparung:
Monate mit niedrigem Bedarf (Juni–August) als Kandidaten für verlängerte
Intervalle. Vergleich mit der Hochsaison.

## Ergebnisse

### Dauerhaft niedrig ausgelastete Standorte

| Kriterium | Anzahl | Anteil |
|---|---:|---:|
| Mittelwert < 50 % UND Maximum < 80 % (nie kritisch) | 9 | 2,0 % |
| Mittelwert < 40 % | 8 | 1,8 % |
| Mittelwert < 50 % (unabhängig vom Maximum) | 67 | 14,9 % |

Nur 9 Standorte sind in einem ganzen Jahr nie kritisch geworden — das ist
weniger als erwartet. Die meisten Standorte hatten mindestens einen kritischen
Messwert.

### Materialprofil der 9 unauffälligen Standorte

Diese 9 Standorte sind überwiegend Braunglas-dominiert (brauner Mittelwert
< 40 %). Sie sind Kandidaten für verlängerte Intervalle oder Bündelung mit
benachbarten Stopps.

### Saisonale Einsparung (Juni–August)

| Monat | Mittelwert | ≥ 80 % | Kritische Stopps/Tag (Median) |
|---|---:|---:|---:|
| 2026-06 | 53,7 % | 24,7 % | ≈ 5 |
| 2026-07 | 61,4 % | 39,2 % | ≈ 7 |
| 2026-08 | 57,5 % | 33,5 % | ≈ 6 |

Gegenüber der Hochsaison (März–April, ≈ 25–30 kritische Stopps/Tag) sind im
Sommer nur 5–8 Stopps/Tag nötig — eine Reduktion um rund 75 %. Das sind die
Monate, in denen Intervalle verlängert und Touren gebündelt werden können.

### Weitere Einsparhebel

1. **Braunglas-Behälter** (69,5 % der Standorte unter 50 % Mittelwert) sind
   Kandidaten für kleinere Behälter oder längere Intervalle (Analyse 28).
2. **Bündelung:** Standorte, die gleichzeitig kritisch werden (Analyse 10,
   Median r = 0,66), können in einer Tour kombiniert werden — spart
   Leerfahrten.
3. **Schwellenwert-Strategie:** nur Standorte mit prognostiziertem Wert ≥ 80 %
   anfahren (13/Tag Median statt 112 bei festem Turnus, Analyse 30).

### Netto-Bilanz (qualitativ)

| Maßnahme | Einsparung | Risiko |
|---|---|---|
| Saisonale Drosselung Jun–Aug | ≈ 75 % weniger Stopps | Niedrig (wenige kritische Standorte) |
| Braunglas-Intervalle verlängern | ≈ 30 % weniger Stopps | Mittel (Braunglas selten, aber nicht nie kritisch) |
| Bündelung gleichzeitiger Stopps | Leerfahrten reduzieren | Niedrig (räumlich, sobald echte Koordinaten vorliegen) |
| Verlängerung bei 9 unauffälligen Standorten | marginal | Niedrig |

## Grenzen

„Einsparung" ist hier eine Mengenabschätzung, keine Kostenrechnung. Ob ein
verlängertes Intervall wirklich spart, hängt von der Fahrstrecke ab, die aus
der CSV nicht ableitbar ist. Die 9 unauffälligen Standorte haben kleine
Messzahlen (Median 6) — sie könnten kritisch sein, ohne dass es gemessen wurde.

## Nächster Schritt

Einsparpotenziale als Szenario (Hochsaison vs. Sommersaison vs. Jahresmittel)
mit dem Mentor durchgehen und die drei Hebel (saisonal, material, Bündelung)
als Roadmap-Punkte für den Prototypen priorisieren.