# 13 – Nachweihnachts-Spitzen

> Die rohe Spitze von +13,5 pp (64,1 % auf 77,6 %) hält im balancierten Panel nur zu 63 % (+8,5 pp), und sie liegt nicht über Weihnachten, sondern in der ersten Messrunde nach dem Jahreswechsel: Am 12.–15.01.2026 sind 59 von 112 Messungen `overfull` (52,7 %) gegenüber 5,7 % im Rest des Januars – bei normaler Anstiegsrate und ohne einen einzigen beobachteten Leerungsrücksetzer.

## Frage

Zeigen die Daten nach Weihnachten besonders viele stark gefüllte Container und damit zusätzlichen Leerungsbedarf – und bleibt dieser Eindruck bestehen, wenn man die wechselnde Messabdeckung kontrolliert?

## Vorgehen

- Datengrundlage: `../glass_fill_levels_anonymized_f.csv`, 11.701 Messungen. `overfull` als 110 % kodiert (tatsächliche Höhe unbekannt). Als „stark gefüllt“ gilt ≥ 80 %, `overfull` zählt mit.
- Drei Zeiträume, wie vorgegeben:
  - **P1** 01.–21.12.2025 (21 Kalendertage)
  - **P2** 22.12.2025–05.01.2026 (15 Tage; entspricht den Weihnachtsferien BW, wie in Analyse 12 belegt)
  - **P3** 06.–31.01.2026 (26 Tage)
- **Annahmen, dokumentiert:** 25./26.12., 01.01. und 06.01. sind gesetzliche Feiertage in BW; an allen vier Tagen liegen **0 Messungen** vor – das ist aus der CSV geprüft, nicht gesetzt. Zusätzlich existiert **05.–11.01.2026 keine einzige Messung** (7 Tage Messloch). Keine Feiertagsdaten wurden hinzuerfunden; die Zeitraumgrenzen stammen aus der Aufgabe.
- **Kennzahlen je Zeitraum × Material:** Messtage, n, n je Kalendertag, Mittelwert roh, Mittelwert im balancierten Panel, Differenz, Anteil ≥ 80 %, `overfull`-Anteil.
- **Balanciertes Panel:** 186 Standort-/Material-Zeitreihen (`Location_id` × `material_type`), die in **allen drei** Zeiträumen mindestens eine Messung haben. Damit ist die Standortzusammensetzung zwischen den Zeiträumen konstant; verglichen werden nur Messungen derselben Behälter.
- **Gepaarter Vergleich zusätzlich:** Für jede Zeitreihe ein Mittelwert je Zeitraum, dann Mittel der individuellen Differenzen (robuster gegen Verschiebungen in der Messhäufigkeit je Behälter).
- **Methodenkritik Abdeckung:** Pearson-/Spearman-Korrelation zwischen Tages-n und Tagesmittel (Dez 2025–Feb 2026), plus Monatsvergleich im Panel über das ganze Jahr.
- Werkzeug: `python3` + pandas.

## Ergebnisse

**Tabelle 1 – Abdeckung der drei Zeiträume**

| Zeitraum | Kalendertage | Messtage | n | n je Kalendertag | Tage ohne Messung |
|---|---:|---:|---:|---:|---:|
| P1 01.–21.12. | 21 | 18 | 952 | 45,3 | 3 |
| P2 22.12.–05.01. | 15 | 11 | 516 | 34,4 | 4 |
| P3 06.–31.01. | 26 | 16 | 672 | 25,8 | 10 |

**Tabelle 2 – Roh gegen balanciertes Panel (186 Serien)**

| Zeitraum | Material | Messtage | n | Ø roh % | Ø Panel % | Δ roh−Panel | ≥ 80 % roh | ≥ 80 % Panel | overfull roh | overfull Panel |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | Braun | 18 | 314 | 31,3 | 36,8 | −5,5 | 8,3 | 11,4 | 0,0 | 0,0 |
| P1 | Grün | 18 | 319 | 74,0 | 77,1 | −3,1 | 53,6 | 56,4 | 0,9 | 3,0 |
| P1 | Weiß | 18 | 319 | 86,4 | 87,4 | −1,0 | 77,1 | 77,9 | 3,1 | 3,8 |
| P1 | **alle** | 18 | 952 | **64,1** | **68,7** | −4,6 | **46,5** | **50,5** | **1,4** | **2,4** |
| P2 | Braun | 11 | 172 | 31,7 | 34,9 | −3,2 | 3,5 | 3,2 | 0,0 | 0,0 |
| P2 | Grün | 11 | 172 | 70,1 | 73,6 | −3,4 | 43,0 | 49,3 | 0,0 | 0,0 |
| P2 | Weiß | 11 | 172 | 82,9 | 84,1 | −1,2 | 74,4 | 81,6 | 0,6 | 0,0 |
| P2 | **alle** | 11 | 516 | **61,6** | **65,8** | −4,3 | **40,3** | **47,2** | **0,2** | **0,0** |
| P3 | Braun | 14 | 193 | 49,3 | 49,5 | −0,2 | 24,9 | 25,8 | 4,1 | 4,8 |
| P3 | Grün | 16 | 233 | 85,7 | 83,2 | +2,5 | 70,8 | 64,3 | 14,6 | 13,1 |
| P3 | Weiß | 16 | 246 | 92,2 | 91,0 | +1,2 | 80,9 | 77,0 | 19,9 | 19,5 |
| P3 | **alle** | 16 | 672 | **77,6** | **77,2** | +0,5 | **61,3** | **58,8** | **13,5** | **13,3** |

Von der rohen Differenz P1 → P3 bleiben im Panel: Ø 8,5 von 13,5 pp (**63 %**), ≥ 80 % 8,3 von 14,8 pp (**56 %**), `overfull` 10,9 von 12,1 pp (**90 %**).

**Tabelle 3 – Gepaarte Differenzen (gleiche Zeitreihe, Mittel der Individualdifferenzen)**

| Paar | Serien | Ø a → Ø b | gepaart | Median | höher / tiefer / gleich |
|---|---:|---|---:|---:|---|
| P1 → P2 | 292 | 68,3 → 60,6 | **−7,7** | −10,0 | 74 / 158 / 60 |
| P2 → P3 | 259 | 65,3 → 76,0 | **+10,7** | +10,0 | 154 / 65 / 40 |
| P1 → P3 | 405 | 67,8 → 79,3 | **+11,5** | +10,0 | 258 / 86 / 61 |

Nach Material (P1 → P3): Braun +16,2 (n = 116), Grün +12,1 (141), Weiß +7,2 (148). **Während der Feiertage selbst (P2) sinkt der Füllstand gegenüber P1 in allen drei Materialien.**

**Tabelle 4 – Methodenkritik: Korrelation Messungen/Tag vs. Tagesmittel (Dez 2025–Feb 2026)**

| Reihe | Messtage | Pearson r | p | Spearman ρ |
|---|---:|---:|---:|---:|
| alle | 61 | −0,15 | 0,25 | −0,16 |
| Braun | 58 | −0,39 | 0,002 | −0,28 |
| Grün | 60 | −0,10 | 0,46 | −0,11 |
| Weiß | 61 | +0,24 | 0,06 | +0,18 |

Die Verzerrung existiert, ist aber **nicht gleichgerichtet**: dünn gemessene Tage liegen bei Braun höher, bei Weiß niedriger, Grün praktisch neutral. Deshalb trägt die Abdeckung nur einen Teil der rohen Differenz – der Rest ist echte Niveauverschiebung.

**Tabelle 5 – Monatsvergleich im Panel (Serien mit Messung in beiden Monaten)**

| Monatspaar | Serien | Ø a → Ø b | gepaart | höher / tiefer |
|---|---:|---|---:|---|
| 11/2025 → 12/2025 | 449 | 61,8 → 63,8 | +2,0 | 189 / 157 |
| **12/2025 → 01/2026** | **479** | **66,4 → 78,4** | **+12,0** | **306 / 112** |
| 01/2026 → 02/2026 | 270 | 81,0 → 75,1 | **−5,9** | 87 / 145 |
| 02/2026 → 03/2026 | 316 | 85,2 → 81,9 | −3,4 | 131 / 153 |
| 05/2026 → 06/2026 | 660 | 77,1 → 49,9 | −27,2 | 96 / 519 |

Der Schritt Dezember → Januar ist der **größte positive Monatsschritt des Jahres** (+12,0 pp) und wird im Februar teilweise zurückgenommen (−5,9 pp).

**Tabelle 6 – Wo die Spitze sitzt (Januar, alle Materialien, roh)**

| Abschnitt | Messtage | n | Ø % | ≥ 80 % | overfull % |
|---|---:|---:|---:|---:|---:|
| 05.–11.01.2026 | 0 | 0 | – | – | – |
| 12.–15.01.2026 | 4 | 112 | 88,1 | 66,1 | **52,7** |
| 16.–31.01.2026 | 12 | 560 | 75,5 | 60,4 | 5,7 |

Am 12.01. allein: n = 18, Ø 100,0 %, 15 von 18 `overfull`. Von den 91 `overfull`-Messungen des Januars fallen **59 (65 %) auf vier Tage**. Im Panel bleibt der Effekt erhalten (P3 ohne 12.–15.01.: Ø 74,9 %, ≥ 80 % 58,1 %, `overfull` 4,5 %).

**Tabelle 7 – Anstiegsrate pp/Tag (nur steigende Segmente, Abstand 7–60 Tage)**

| Segment | n | Median-Rate | Median-Abstand |
|---|---:|---:|---:|
| 22.12.–15.01. | 202 | +0,92 | 20,5 d |
| Nov–Anfang Dez | 494 | +0,82 | 28 d |
| 16.01.–28.02. | 503 | +0,83 | 35 d |
| übriges Jahr | 2.383 | +0,95 | 28 d |

Die Zunahme pro Tag ist über den Jahreswechsel **nicht erhöht**. Dafür fehlen die Rücksetzer: Bei Übergängen mit 7–14 Tagen Abstand ist die Median-Rate im Jahresmittel **−1,00** (Leerungen dominieren), im Fenster 05.–18.01. dagegen **+1,41** (n = 26). Von den 40 Übergängen mit Vorwert ab 28.12. steigt der Füllstand über im Median 13 Tage im Mittel von 72,5 % auf 87,0 % – ohne Zwischenleerung.

## Interpretation

- **Die Spitze ist real, aber nicht weihnachtlich.** Roh steigt der Füllstand von 64,1 % auf 77,6 %, im balancierten Panel bleiben davon 8,5 pp. Der Zuwachs entsteht jedoch **nicht** zwischen dem 22.12. und dem 05.01. – dort fällt das Panel-Niveau von 68,7 % auf 65,8 % (−7,7 pp gepaart, 158 von 292 Serien tiefer). Der Sprung passiert zwischen dem letzten Messwert vor dem Messloch und der Runde am 12.01.
- **Es ist ein Auffüll-Effekt, kein Zulauf-Effekt.** Die Anstiegsrate pro Tag liegt über den Jahreswechsel bei 0,92 pp/Tag gegenüber 0,82–0,95 im Vergleichszeitraum, also im Normalbereich. Was fehlt, sind Leerungsrücksetzer: In normalen Wochen bedeutet ein kurzer Messabstand von 7–14 Tagen im Median einen Rückgang (−1,00 pp/Tag), im Januarfenster dagegen einen Anstieg (+1,41). Die Container wurden also über den Jahreswechsel nicht geleert und liefen mit normaler Geschwindigkeit voll.
- **Der zusätzliche Leerungsbedarf konzentriert sich auf eine Woche, nicht auf den Januar.** 65 % aller `overfull`-Messungen des Januars liegen in den vier Tagen 12.–15.01.; zwei Wochen später sind es 5,7 %. Für die Tourenplanung heißt das: eine Sonderspitze in der ersten Januarrunde, kein flächig erhöhter Monat.
- **Der Monatsvergleich stützt eine Nachweihnachtskomponente, aber eine gedämpfte.** Dezember → Januar ist mit +12,0 pp der größte positive Monatsschritt des Jahres, im Februar gehen −5,9 pp wieder verloren. Ein Teil davon ist der Jahresanstieg (Oktober bis März steigt der Füllstand insgesamt), ein Teil das Auffüllen über den Jahreswechsel – beides ist mit Füllständen allein nicht trennbar.
- **Weiß ist der kritische Fall, und dort schrumpft die Spitze am stärksten.** Roh steigt der ≥ 80 %-Anteil von 77,1 % auf 80,9 %, im Panel dagegen von 77,9 % auf 77,0 % – praktisch **kein Anstieg**. Der rohe Weiß-Sprung ist überwiegend ein Zusammensetzungsartefakt. `overfull` steigt dagegen auch im Panel deutlich (3,8 % auf 19,5 %), weil das Kappen bei 110 % die Verteilung oben abschneidet.
- **Die Methodenkritik ist hier nicht Kosmetik.** Die Abdeckung fällt von 45,3 auf 25,8 Messungen pro Kalendertag, und genau die dünnsten Tage liegen in P3. Weil die Korrelation n vs. Tagesmittel je Material unterschiedlich vorzeichenbehaftet ist (−0,39 Braun, +0,24 Weiß), verschiebt die Abdeckung die Materialmittel in verschiedene Richtungen. Erst das Panel macht die Materialaussagen vergleichbar.

## Grenzen

- **Kein Leerungsdatum.** „Kein Rücksetzer beobachtet“ ist nicht „nicht geleert“. Zwischen 05. und 11.01. wurde überhaupt nicht gemessen; ob in dieser Woche geleert wurde, sagt der Datensatz nicht. Die Aussage „Leerung fiel aus“ ist eine Mechanik-Hypothese, keine Beobachtung.
- **Das Messloch ist mit der Ursache confounded.** Fehlende Messungen und fehlende Leerungen treten in derselben Woche auf – vermutlich derselbe Betriebsstillstand. Auffüllung und Messausfall sind daher grundsätzlich nicht trennbar.
- **Kleine Panel-Zellen.** Das Tripel-Panel hat je Zeitraum nur 62–104 Messungen (1,1–1,6 je Serie). Die gepaarten Differenzen stützen sich zusätzlich auf 405 Serien, aber mit je zwei bis drei Messpunkten pro Zeitraum; die 10-pp-Rasterung begrenzt die Auflösung.
- **Ein Winter, keine Wiederholung.** Weihnachten 2025/26 kommt im Datensatz genau einmal vor. Signifikanztests über eine Saison wären nicht belastbar und werden nicht berichtet; alle p-Werte oben beziehen sich nur auf die Tageskorrelation.
- **`overfull` ist gekappt.** Alle Werte ab 110 % sind ununterscheidbar; wie voll ein überfüllter Behälter tatsächlich war, ist unbekannt. Der `overfull`-Anteil ist dadurch der empfindlichste, aber auch der gröbste Indikator.
- **Saison und Feiertag nicht trennbar:** Oktober bis März ist die Aufstiegsphase im Jahresverlauf (Monatsmittel 55,6 % bis 85,2 %); ohne Mehrjahresdaten lässt sich der Weihnachtsanteil am Januarhub nicht isolieren.
- Aggregate über Messtage sind durch die jeweils gemessene Teilmenge verzerrt; `Location_id` bezeichnet einen Standort, nicht einen einzelnen Behälter; Koordinaten sind synthetisch.

## Nächster Schritt

Leerungsereignisse (Datum, Standort, Material, Menge) für Dezember 2025 bis Februar 2026 beschaffen und für die 112 Messungen vom 12.–15.01. prüfen, wie viele Tage seit der letzten dokumentierten Leerung vergangen waren – damit ließe sich „Betriebsstillstand“ von „Lieferengpass beim Leerfahrzeug“ trennen und die Sonderspitze gezielt einplanen.
