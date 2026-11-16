# 10 – Standortkopplung: Bewegen sich Braun, Grün und Weiß gemeinsam?

> An 1.111 auswertbaren Materialpaaren korrelieren die Füllstände an gemeinsamen Messtagen im Median mit r = 0,66, und Leerungen treffen an gemeinsamen Tagen 1,6-mal häufiger zusammen als unter Unabhängigkeit erwartet (26,3 % statt 16,3 %) – die drei Behälter eines Standorts verhalten sich überwiegend wie eine Einheit, mit Grün–Weiß als stärkstem und Braun–Weiß als schwächstem Paar.

## Frage

Steigen und fallen Braun-, Grün- und Weißglas am selben Standort gemeinsam – und deutet das auf lokale Treiber (gleiches Einzugsgebiet, gleiches Nutzerverhalten) oder auf gemeinsame Leerungszyklen?

## Vorgehen

- Datengrundlage: `../glass_fill_levels_anonymized_f.csv`, 11.701 Messungen, 449 Standorte. `overfull` als 110 % kodiert (tatsächliche Höhe unbekannt).
- **Grundmenge:** 448 Standorte mit ≥ 2 Materialien (441 mit allen drei, 7 mit zwei); daraus 1.330 Materialpaare.
- **Gemeinsame Messtage:** je Standort Paare von Messungen, die exakt auf dasselbe `date` fallen. Nur Paare mit ≥ 4 gemeinsamen Tagen werden korreliert (Pearson, Füllstand in %). Keine Doppelmessungen je Zeitreihe/Tag vorhanden.
- **Ergebnisumfang:** 1.116 Paare mit ≥ 4 gemeinsamen Tagen (83,9 %), davon 1.111 mit definiertem r (5 Paare haben an allen gemeinsamen Tagen denselben Wert, SD = 0, und sind ausgeschlossen). Summe der gemeinsamen Tage 9.776, Median 8 pro Paar (Q25 6, Q75 11).
- **Leerungs-Koinzidenz:** je Zeitreihe Differenz zur Vormessung; negativer Sprung = Leerungsindiz. An gemeinsamen Tagen, an denen für beide Materialien eine Vormessung existiert, wird gezählt, ob beide negativ sind. Erwartungswert unter Unabhängigkeit = Produkt der beiden Randraten mal Anzahl Tage (hypergeometrisch, da die Randhäufigkeiten fixiert sind). Zusätzlich 2.000 Permutationsläufe mit fixierten Randhäufigkeiten je Paar.
- **Sensitivität:** nur Paare mit ≥ 6 / ≥ 8 / ≥ 10 gemeinsamen Tagen; Teilstichprobe mit Vormessungen am selben Tag (± 1 Tag), also identischem Beobachtungsfenster.
- Werkzeug: `python3` mit pandas und numpy.

## Ergebnisse

**Tabelle 1 – Korrelation je Materialpaar (gemeinsame Messtage, ≥ 4 Tage)**

| Paar | Paare | Median r | Mittel r | Anteil r > 0,5 | Anteil r > 0,7 | Anteil r < 0 | Anteil r > 0 | Median gemeinsame Tage |
|---|---|---|---|---|---|---|---|---|
| Braun–Grün | 352 | 0,595 | 0,500 | 59,4 % | 36,1 % | 10,2 % | 89,5 % | 7 |
| Braun–Weiß | 352 | 0,575 | 0,500 | 62,2 % | 31,2 % | 8,5 % | 89,8 % | 7 |
| Grün–Weiß | 407 | 0,751 | 0,673 | 83,0 % | 57,5 % | 3,4 % | 96,6 % | 9 |
| **alle** | **1.111** | **0,655** | **0,563** | **68,9 %** | **42,4 %** | **7,2 %** | **92,2 %** | **8** |

Verteilung über alle Paare: 5 %-Quantil −0,14 · Q25 0,44 · Median 0,66 · Q75 0,80 · 95 %-Quantil 0,93. |r| > 0,9 bei 10,4 % der Paare.

**Tabelle 2 – Sensitivität gegen dünne Überlappung**

| Teilmenge | Paare | Median r | r > 0,5 | r < 0 |
|---|---|---|---|---|
| ≥ 4 gemeinsame Tage | 1.111 | 0,655 | 68,9 % | 7,2 % |
| ≥ 6 gemeinsame Tage | 842 | 0,658 | 71,5 % | 4,8 % |
| ≥ 8 gemeinsame Tage | 591 | 0,650 | 73,4 % | 3,6 % |
| ≥ 10 gemeinsame Tage | 394 | 0,652 | 74,1 % | 3,0 % |
| nur genau 4 Tage | 132 | 0,610 | 56,8 % | 16,7 % |

Der Median bleibt stabil; nur die Negativquote sinkt mit mehr Stützpunkten (kurze Reihen produzieren Scheinkorrelationen in beide Richtungen).

**Tabelle 3 – Gleichzeitige negative Sprünge an gemeinsamen Tagen**

| Paar | Beobachtbare Tage | beide negativ | beobachtet | erwartet (unabh.) | Verhältnis |
|---|---|---|---|---|---|
| Braun–Grün | 2.630 | 647 | 24,6 % | 16,1 % | 1,52 |
| Braun–Weiß | 2.648 | 580 | 21,9 % | 14,3 % | 1,53 |
| Grün–Weiß | 3.688 | 1.128 | 30,6 % | 17,9 % | 1,71 |
| **alle** | **8.966** | **2.355** | **26,3 %** | **16,3 %** | **1,61** |

- Randraten: 40,9 % der Tage mit Vormessung sind negativ (Material A), 38,9 % (Material B); Median der Reihen-Negativrate 0,40 (Braun), 0,44 (Grün), 0,40 (Weiß).
- Bedingt: fällt A, fällt B in **64,2 %** der Fälle (Basisrate 38,9 %) – Faktor 1,65.
- Permutation (2.000 Läufe, Randhäufigkeiten fixiert): Erwartung 1.465 ± 22 gleichzeitige Ereignisse, beobachtet 2.355, z ≈ 40,3.
- Gleiches Beobachtungsfenster (Vormessungen beider Materialien ≤ 1 Tag auseinander): 7.304 Tage, 28,1 % beide negativ, erwartet 17,3 % – Verhältnis 1,62. Der Effekt ist also nicht nur ein Artefakt unterschiedlich langer Intervalle.
- Messpraxis: von 4.468 Standort-Tagen sind 3.061 mit allen drei Materialien am selben Tag belegt, 1.111 mit zwei, 296 mit einem.

**Tabelle 4 – Standortniveau (408 Standorte mit ≥ 1 auswertbarem Paar)**

| Kennzahl | Wert |
|---|---|
| Ø r je Standort: P10 / Q25 / Median / Q75 / P90 | 0,25 / 0,44 / 0,64 / 0,76 / 0,87 |
| Standorte mit Ø r > 0,5 | 70,1 % |
| Standorte mit Ø r > 0,8 | 17,4 % |
| Standorte mit Ø r < 0,2 | 9,1 % |
| Standorte mit Ø r < 0 | 4,7 % |
| Standorte mit drei Paaren (n = 351): alle drei r > 0,5 | 43,9 % |
| davon mindestens ein negatives Paar | 16,8 % |

Zusammenhang mit dem Niveau: Spearman(Ø r, Abstand Weiß − Braun) = −0,30; mit dem Weiß-Niveau −0,22, mit Braun +0,13, mit Grün +0,02. Hohe Kopplung ist also nicht bloß ein Standort mit besonders vollem Weißglas.

**Tabelle 5 – 10 Standorte mit der höchsten Kopplung (je drei Paare)**

| Standort | Ø r | min–max r | Tage | Ø Braun | Ø Grün | Ø Weiß |
|---|---|---|---|---|---|---|
| 4c52d626 | 0,96 | 0,94–0,98 | 6 | 34,0 | 37,1 | 53,3 |
| 3fdaa1bd | 0,94 | 0,90–0,97 | 9 | 30,0 | 59,0 | 70,0 |
| 690a7ad6 | 0,94 | 0,85–1,00 | 7 | 30,0 | 78,6 | 81,4 |
| 42f76318 | 0,94 | 0,91–0,99 | 6 | 50,0 | 71,7 | 81,7 |
| efc8174e | 0,93 | 0,92–0,94 | 11 | 20,0 | 54,6 | 65,5 |
| 7d784047 | 0,92 | 0,91–0,94 | 9 | 58,0 | 56,7 | 70,0 |
| 7d069a27 | 0,92 | 0,86–0,98 | 4 | 60,0 | 100,0 | 87,5 |
| b344ad00 | 0,92 | 0,87–0,97 | 7 | 38,3 | 64,3 | 74,4 |
| 6cc592ff | 0,92 | 0,85–0,95 | 6 | 21,7 | 63,3 | 60,0 |
| 1a1377dc | 0,91 | 0,90–0,91 | 4 | 40,0 | 52,5 | 74,0 |

**Tabelle 6 – 10 Standorte mit der niedrigsten Kopplung (je drei Paare)**

| Standort | Ø r | min–max r | Tage | Ø Braun | Ø Grün | Ø Weiß |
|---|---|---|---|---|---|---|
| 32d77ab0 | −0,35 | −1,00–0,91 | 6 | 32,5 | 45,0 | 91,4 |
| 77ba55cc | −0,32 | −0,85–0,31 | 6 | 27,5 | 71,7 | 84,3 |
| 696f6a25 | −0,31 | −0,77–0,52 | 4 | 27,5 | 87,5 | 82,0 |
| 36af8e94 | −0,22 | −1,00–0,86 | 6 | 12,5 | 36,7 | 53,3 |
| 8644edba | −0,20 | −0,70–0,45 | 6 | 25,0 | 40,0 | 81,4 |
| 7f2c0772 | −0,16 | −0,93–0,56 | 5 | 22,5 | 48,0 | 70,0 |
| d76838d8 | −0,16 | −0,57–0,38 | 6 | 37,5 | 40,0 | 80,0 |
| 36a500a8 | −0,15 | −0,76–0,36 | 5 | 30,0 | 52,5 | 83,3 |
| d4b8ebea | −0,14 | −0,86–0,34 | 10 | 36,7 | 72,0 | 85,5 |
| 4a96689f | −0,11 | −0,60–0,57 | 9 | 18,6 | 66,7 | 82,0 |

Die negativen Standorte haben durchweg ein großes Gefälle Braun zu Weiß (41–63 pp) – dort entkoppelt sich der träge Braunglas-Behälter vom schnell laufenden Weißglas, und einzelne Leerungen dominieren die kurze Reihe.

## Interpretation

- **Kopplung ist der Normalfall, nicht die Ausnahme.** 92 % der Paare korrelieren positiv, 69 % über 0,5, und 70 % der Standorte liegen im Standortmittel über 0,5. Ein Standort ist überwiegend eine Betriebseinheit: gleiches Einzugsgebiet, gleiche Bringfrequenz der Anwohner, gleicher Messtermin.
- **Grün–Weiß ist das festeste Paar** (Median 0,75, 83 % über 0,5). Beide liegen nahe der Sättigung; sie laufen gemeinsam gegen die 100 %/`overfull`-Decke. Ein Teil dieser Kopplung ist Deckeneffekt, nicht gemeinsamer Treiber.
- **Braun ist der Ausreißer im Standort.** Braun–Weiß (0,575) und Braun–Grün (0,595) sind deutlich schwächer, mit 8,5–10,2 % negativen Paaren. Braun füllt langsamer, wird seltener gemessen und wird oft erst geleert, wenn Weiß schon mehrfach geleert wurde.
- **Leerungen sind gebündelt.** An gemeinsamen Tagen fallen negative Sprünge 1,6-mal häufiger zusammen als unter Unabhängigkeit; die Koinzidenz ist bei Grün–Weiß am stärksten (1,71) und bleibt im Teilsample mit identischem Beobachtungsfenster erhalten (1,62). Das ist der stärkste Hinweis auf gebündelte Anfahrten: Wer Weiß leert, leert häufig auch Grün und Braun.
- **Entkoppelte Standorte sind Braun-lastig.** Die 10 schwächsten Standorte haben ein Weiß-Braun-Gefälle von 41–63 pp. Dort lohnt keine gemeinsame Tourenplanung über alle Materialien; dort braucht Braun einen eigenen Auslöser.
- **Operativ:** Standortweise statt materialweiser Planung. Für die 70 % gekoppelten Standorte reicht ein Auslöser (z. B. Weiß), die übrigen Materialien folgen; für die 9 % mit Ø r < 0,2 braucht jedes Material einen eigenen Schwellwert.

## Grenzen

- **Pearson auf 4–11 Punkten ist fragil.** Bei n = 4 ist r = 0,5 nicht signifikant (p ≈ 0,39); 132 Paare (11,9 %) haben genau 4 gemeinsame Tage, dort liegt die Negativquote bei 16,7 % statt 3,6 % bei ≥ 8 Tagen. Die Rangfolge der Materialpaare ist über alle Sensitivitätsstufen stabil, einzelne Standortwerte nicht.
- **16,1 % der Paare (214) fallen aus der Auswertung**, weil sie weniger als 4 gemeinsame Tage haben. Das sind systematisch schwach beobachtete Standorte; die Kopplung der Gesamtheit ist dadurch eher überschätzt.
- **Koinzidenz ist nicht Kausalität, und der Hauptteil ist ein Messartefakt.** Ein negativer Sprung heißt „seit der letzten Messung dieser Zeitreihe geleert, unbekannt wann und wie oft“. Da beide Materialien meist am selben Tag gemessen werden, teilen sie das Beobachtungsfenster; bei rund 41 Tagen Abstand und üblicher Leerungsfrequenz ist Koinkidenz mechanisch wahrscheinlich. Das Teilsample mit ± 1 Tag Fensterunterschied reduziert, beseitigt den Effekt aber nicht. Ohne Leerungsereignisse (Datum, Fahrzeug, Tour) lässt sich „gebündelte Leerung“ nicht belegen, nur plausibilisieren.
- **10-pp-Raster und Deckeneffekt.** Alle Werte liegen auf 0,10,…,100 oder 110; bei zwei Reihen, die überwiegend zwischen 80 und 110 pendeln, entsteht hohe Korrelation allein durch die Obergrenze. `overfull` = 110 % ist eine Untergrenze der tatsächlichen Füllhöhe.
- **Aggregat über Messtage verzerrt.** Standortmittel sind ungewichtet über die zufällig gemessene Teilmenge; Standorte mit mehr Messungen gehen stärker in die Paarstatistik ein.
- **Keine Standortmerkmale.** Koordinaten sind synthetisch (`source=synthetic_placeholder`), Einwohnerzahl, Behältergröße, Nutzungsart und Anfahrtshistorie fehlen – „lokaler Treiber“ bleibt hier eine Blackbox, die sich nur indirekt als Standorteffekt zeigt.
- Die Standort-IDs sind anonymisiert; die Tabellen 5 und 6 sind ohne Standortregister nicht auflösbar.

## Nächster Schritt

Für die 32 Standorte mit drei Paaren und Ø r < 0,2 die vollständigen Zeitreihen (Datum, Material, Füllstand, Vormessung, Abstand in Tagen) als Tabelle exportieren und je Standort prüfen, ob die Entkopplung aus einzelnen Leerungen eines Materials oder aus auseinanderlaufenden Messzeitpunkten entsteht – erst danach ist entscheidbar, ob diese Standorte einen materialweisen Auslöser brauchen.
