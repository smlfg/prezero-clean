# 11 – Saisonale Nachfrage

> Das mittlere Füllniveau schwankt zwischen 53,7% (Juni) und 85,2% (März) — ein Abstand von 31,5 Prozentpunkten; der Effekt bleibt nach Standortbereinigung praktisch unverändert (mittlere Abweichung 0,5 pp), ist also kein Kompositionseffekt.

## Frage

Wann ist mit höherem, wann mit niedrigerem Glasaufkommen zu rechnen — und trägt der Monatseffekt einer Standortbereinigung stand?

## Vorgehen

- Datensatz `glass_fill_levels_anonymized_f.csv`, 11.701 Messungen, 2025-10-17 bis 2026-09-30.
- `overfull` als 110 kodiert (tatsächliche Höhe unbekannt); Kennzahlen: Mittelwert, Median, Anteil ≥ 80%, `overfull`-Anteil, Anzahl Messungen.
- Monatsaggregate gesamt und je `material_type`.
- Feinere Auflösung: ISO-Kalenderwoche (Jahr + Woche), nur Wochen mit ≥ 30 Messungen ausgewiesen (48 von 50 Wochen, 52 Messzeilen entfallen dadurch).
- **Kompositionstest 1 (within-Zentrierung):** je Messung die Abweichung vom Standortmittel (`Location_id`) gebildet, Monatsmittel dieser Abweichungen plus Gesamtmittel 66,0% = standortbereinigtes Monatsmittel. Differenz zum Rohmittel ausgewiesen.
- **Kompositionstest 2 (fixes Panel):** nur die 42 Standorte, die in allen 12 Monaten gemessen wurden.
- **Kompositionstest 3 (Paarvergleich):** je Monatspaar Mittel der Within-Standort-Differenz über alle Standorte, die in beiden Monaten gemessen wurden (nur Paare mit ≥ 20 Standorten).

## Ergebnisse

### Monatsaggregate gesamt (n = 11.701)

| Monat | n | Mittel | Median | ≥ 80% | overfull | Standorte | Messtage |
|---|---|---|---|---|---|---|---|
| 2025-10 | 741 | 55,6 | 50 | 28,6% | 0,4% | 239 | 11 |
| 2025-11 | 656 | 59,5 | 60 | 38,6% | 2,1% | 194 | 17 |
| 2025-12 | 1.357 | 62,9 | 70 | 43,8% | 1,0% | 327 | 26 |
| 2026-01 | 783 | 76,1 | 90 | 59,9% | 11,6% | 225 | 19 |
| 2026-02 | 657 | 76,5 | 90 | 58,8% | 12,9% | 219 | 16 |
| 2026-03 | 776 | **85,2** | 90 | **68,3%** | **37,6%** | 328 | 23 |
| 2026-04 | 896 | 82,3 | 90 | 67,6% | 23,3% | 301 | 18 |
| 2026-05 | 951 | 74,4 | 80 | 54,6% | 22,7% | 296 | 19 |
| 2026-06 | 1.501 | **53,7** | 50 | **24,7%** | 5,2% | 413 | 21 |
| 2026-07 | 1.310 | 61,4 | 60 | 39,2% | 5,0% | 342 | 22 |
| 2026-08 | 1.215 | 57,5 | 60 | 33,5% | 2,8% | 353 | 21 |
| 2026-09 | 858 | 64,1 | 60 | 42,7% | 10,6% | 270 | 16 |
| **gesamt** | 11.701 | 66,0 | 70 | 44,7% | 10,2% | 449 | 229 |

### Kompositionstest: Roh- vs. standortbereinigtes Monatsmittel

| Monat | Roh | bereinigt | Differenz |
|---|---|---|---|
| 2025-10 | 55,6 | 55,6 | −0,0 |
| 2025-11 | 59,5 | 59,9 | −0,4 |
| 2025-12 | 62,9 | 62,5 | +0,5 |
| 2026-01 | 76,1 | 75,2 | +0,9 |
| 2026-02 | 76,5 | 75,3 | +1,2 |
| 2026-03 | 85,2 | 84,7 | +0,5 |
| 2026-04 | 82,3 | 82,7 | −0,4 |
| 2026-05 | 74,4 | 74,4 | −0,0 |
| 2026-06 | 53,7 | 54,7 | −1,0 |
| 2026-07 | 61,4 | 61,6 | −0,2 |
| 2026-08 | 57,5 | 57,9 | −0,4 |
| 2026-09 | 64,1 | 63,7 | +0,4 |

Korrelation der beiden Reihen 0,999; mittlere absolute Differenz 0,47 pp, Maximum 1,23 pp (Februar).

**Fixes Panel (42 Standorte, alle 12 Monate):** Monatsmittel 57,3 · 71,0 · 67,8 · 79,7 · 79,0 · 89,1 · 89,1 · 77,0 · 54,5 · 70,7 · 57,7 · 67,4 — Korrelation mit der Gesamtreihe 0,957, gleiche Form (Hoch März/April, Tief Juni). Das Panel liegt durchweg 0,2 bis 11,5 pp höher: häufiger gemessene Standorte sind im Mittel voller.

**Paarvergleich (66 Monatspaare mit ≥ 20 gemeinsamen Standorten):** Extremwerte sind März→Juni −31,6 pp (316 Standorte), April→Juni −28,8, März→August −27,6, sowie Oktober→März +32,8 und November→März +26,2. Der Monatseffekt ist also an denselben Standorten messbar, nicht nur zwischen Standortgruppen.

### Monatsmittel je Material (Mittel / `overfull`-Anteil)

| Monat | braun | grün | weiß |
|---|---|---|---|
| 2025-10 | 28,3 / 0,0% | 61,0 / 0,0% | 76,5 / 1,2% |
| 2025-11 | 28,4 / 0,9% | 67,8 / 1,8% | 82,1 / 3,6% |
| 2025-12 | 31,3 / 0,0% | 72,1 / 0,7% | 85,1 / 2,4% |
| 2026-01 | 46,7 / 3,5% | **84,9** / 12,6% | 91,5 / 17,3% |
| 2026-02 | 49,8 / 4,1% | 82,9 / 14,7% | 91,7 / 18,2% |
| 2026-03 | **67,8** / 25,6% | 81,8 / 29,5% | 90,8 / 45,3% |
| 2026-04 | 66,5 / 8,4% | 81,3 / 18,7% | **92,0** / 35,7% |
| 2026-05 | 55,5 / 11,6% | 75,5 / 20,8% | 88,0 / 33,3% |
| 2026-06 | 32,9 / 1,8% | 50,5 / 3,1% | 64,2 / 8,4% |
| 2026-07 | 36,7 / 0,5% | 63,6 / 3,8% | 81,2 / 10,2% |
| 2026-08 | 32,4 / 0,3% | 58,5 / 2,1% | 77,4 / 5,5% |
| 2026-09 | 37,3 / 4,1% | 64,5 / 8,5% | 82,2 / 17,2% |

Braun und Grün erreichen ihr Maximum im März, Weiß im April; das Minimum liegt für Grün und Weiß im Juni, für Braun im Oktober. Die Phase ist bei allen drei Materialien dieselbe, nur das Niveau verschiebt sich.

### ISO-Kalenderwochen (nur Wochen mit ≥ 30 Messungen)

| Woche | n | Mittel | ≥ 80% | overfull | Woche | n | Mittel | ≥ 80% | overfull |
|---|---|---|---|---|---|---|---|---|---|
| 2025-W43 | 354 | 56,5 | 28% | 0% | 2025-W44 | 364 | 53,9 | 28% | 0% |
| 2025-W45 | 270 | 49,6 | 20% | 0% | 2025-W46 | 84 | 51,5 | 33% | 0% |
| 2025-W47 | 30 | 79,0 | 67% | 17% | 2025-W48 | 272 | 69,7 | 55% | 3% |
| 2025-W49 | 284 | 71,6 | 58% | 3% | 2025-W50 | 304 | 61,9 | 46% | 1% |
| 2025-W51 | 364 | 60,1 | 38% | 0% | 2025-W52 | 210 | 57,7 | 32% | 0% |
| 2026-W01 | 306 | 64,2 | 46% | 0% | 2026-W03 | 137 | 88,5 | 67% | 53% |
| 2026-W04 | 275 | 73,1 | 55% | 3% | 2026-W05 | 260 | 76,7 | 65% | 4% |
| 2026-W06 | 361 | 71,2 | 51% | 2% | 2026-W08 | 102 | 74,1 | 56% | 6% |
| 2026-W09 | 165 | 90,3 | 77% | 44% | 2026-W10 | 212 | **91,3** | 78% | 48% |
| 2026-W11 | 240 | 86,1 | 72% | 41% | 2026-W12 | 123 | 84,7 | 67% | 37% |
| 2026-W13 | 154 | 79,1 | 56% | 21% | 2026-W14 | 119 | 84,2 | 69% | 34% |
| 2026-W15 | 105 | 79,0 | 58% | 30% | 2026-W16 | 188 | 86,6 | 78% | 19% |
| 2026-W17 | 234 | 80,1 | 66% | 18% | 2026-W18 | 297 | 80,3 | 62% | 25% |
| 2026-W19 | 222 | 72,3 | 54% | 20% | 2026-W20 | 302 | 78,1 | 60% | 27% |
| 2026-W21 | 267 | 70,0 | 51% | 16% | 2026-W22 | 160 | 77,5 | 51% | 29% |
| 2026-W23 | 449 | 64,5 | 40% | 10% | 2026-W24 | 530 | **47,8** | 16% | 3% |
| 2026-W25 | 240 | 49,7 | 17% | 2% | 2026-W26 | 215 | 51,4 | 25% | 5% |
| 2026-W27 | 205 | 56,5 | 28% | 4% | 2026-W28 | 323 | 59,4 | 35% | 4% |
| 2026-W29 | 241 | 63,4 | 47% | 4% | 2026-W30 | 350 | 59,9 | 36% | 6% |
| 2026-W31 | 258 | 65,2 | 45% | 6% | 2026-W32 | 293 | 56,7 | 35% | 4% |
| 2026-W33 | 296 | 55,3 | 31% | 3% | 2026-W34 | 296 | 59,6 | 37% | 2% |
| 2026-W35 | 275 | 60,5 | 35% | 1% | 2026-W36 | 203 | 58,5 | 33% | 7% |
| 2026-W37 | 209 | 62,2 | 44% | 4% | 2026-W38 | 213 | 59,0 | 36% | 3% |
| 2026-W39 | 117 | 68,4 | 49% | 4% | 2026-W40 | 171 | 71,0 | 48% | 36% |

Wochenspanne 47,8 (W24) bis 91,3 (W10) = 43,5 pp. Der Übergang ins Hoch ist Wochen, nicht Monate scharf: W05 76,7 → W09 90,3; der Absturz von W22 77,5 auf W24 47,8. Die Monatsgrenzen glätten diese Kanten; der Monatsmittelwert für März (85,2) verdeckt, dass W09–W10 der eigentliche Peak sind.

## Interpretation

- **Ein saisonaler Gang ist belegt, die Komposition ist es nicht.** Standortbereinigung verändert das Monatsprofil um höchstens 1,2 pp. Das Muster liegt also in den Standorten selbst, nicht darin, welche Standorte in welchem Monat gemessen wurden.
- **Hochphase Februar bis Mai.** Das ist das Winter-/Frühjahrsfenster: 26,6% aller Messungen fallen auf Jan–Apr, aber 21,8% davon sind `overfull` (als 110% kodiert, tatsächliche Höhe unbekannt) gegenüber 6,0% im Rest des Jahres. März ist mit 37,6% `overfull` der kritischste Monat.
- **Tiefphase Juni bis August.** Juni ist mit 53,7% Mittel und 5,2% `overfull` der entspannteste Monat; W24 (47,8%, 16% ≥ 80%) ist die klarste Einzelwoche. In diesem Fenster ist Luft für längere Intervalle.
- **Planungsempfehlung, so weit die Daten tragen:** Zusatzfahrten bzw. kürzeres Intervall für **Februar bis Mai**, mit Schwerpunkt auf der zweiten Märzhälfte (W09–W16 durchgehend ≥ 79%) und der ersten Aprilhälfte. Gedrosseltes Intervall für **Juni bis August**, beginnend ab W24. Oktober bis Dezember und September liegen im Mittelfeld und brauchen keine Sonderregel.
- **Material spezifisch:** Weiß läuft früher voll (Maximum schon im April, 92,0%) und bleibt im Tief bei 64,2% — Weiß braucht die Verlängerung im Sommer am wenigsten. Braun ist das empfindlichste Material im Frühjahr (Sprung von 31,3% im Dezember auf 67,8% im März, mehr als Verdopplung) und reagiert am stärksten auf die Saison.
- **Wochensteuerung statt Monatssteuerung:** Der Übergang passiert innerhalb von zwei bis drei Wochen. Eine Regel, die am Monatsersten umschaltet, ist entweder drei Wochen zu spät (Frühjahr) oder drei Wochen zu früh (Sommer).

## Grenzen

- **Nur ein Jahr.** Das Muster ist ein einziger Zyklus. Saison und Trend sind nicht trennbar; ein einmaliger Ausreißer (etwa ein Sondereffekt im Frühjahr 2026) sieht identisch aus wie Saisonalität. Für eine belastbare Regel braucht es mindestens zwei, besser drei Jahre.
- **Oktober 2025 ist unvollständig** (Daten ab 17.10., 11 Messtage) und damit als Monatswert nicht mit den übrigen vergleichbar; er ist im Hoch-/Tiefvergleich deshalb nicht verwendet.
- **Messanlass ist nicht erhoben.** Wann ein Behälter gemessen wird, hängt vom Leerungsturnus ab. Ein niedriger Juni-Wert kann auch bedeuten, dass häufiger direkt nach der Leerung gemessen wurde — Juni hat mit 1.501 Messungen und 413 Standorten die meisten Messungen des Jahres, und über die Monate korreliert die Messanzahl mit dem Mittelwert (−0,49). Auf Tagesebene ist der Zusammenhang schwach (−0,15), der Verdacht ist also nicht ausgeräumt, aber auch nicht bestätigt.
- **Wetter, Feiertage, Tourismus, Veranstaltungen** fehlen vollständig. Ob die Hochphase auf Weihnachten/Neujahr, auf Kälte (mehr Flaschenwein/Glühwein) oder auf den Leerungskalender zurückgeht, ist aus diesen Daten nicht entscheidbar.
- **Kleine Wochen:** W47/2025 (n = 30), W08 (102), W15 (105), W39 (117) tragen einzelne Ausreißer stärker; W40/2026 (35,7% `overfull` bei 171 Messungen) beruht wesentlich auf dem 29.09. (52,3% bei 65 Messungen).
- Anonymisierte IDs, synthetische Koordinaten: keine Aussage über Regionen, Stadtteile oder Wetterzonen möglich.

## Nächster Schritt

Zwei weitere Messjahre nachziehen und dasselbe Monats-/Wochenprofil darauf prüfen — erst wenn sich Hoch- und Tiefphase wiederholen, wird aus dem Ein-Jahres-Muster eine belastbare Intervallregel.
