# 08 – Standortvergleich: starke und schwache Standorte

> Zwischen dem schwächsten und dem stärksten Zehntel der 449 Standorte liegen 25,8 Prozentpunkte mittlerer Füllstand (50,0 % vs. 75,8 %), aber der Standort erklärt nur 8,6 % der Messvarianz gegenüber 28,7 % durch das Material, und die Rangfolge ist zwischen zwei Halbjahren nur schwach stabil (Spearman ρ = 0,30).

## Frage

Welche Standorte sind über den gesamten Zeitraum besonders stark, welche besonders schwach ausgelastet? Wie verteilt sich das über alle 449 Standorte, wie stabil ist die Rangfolge über die Zeit, und wie viel der Streuung entfällt auf den Standort statt auf das Material?

## Vorgehen

- Datengrundlage: `../glass_fill_levels_anonymized_f.csv`, 11.701 Messungen, 449 `Location_id`, 2025-10-17 bis 2026-09-30. `overfull` als 110 % kodiert (tatsächliche Höhe unbekannt).
- **Standortaggregat** je `Location_id` über alle Materialien: Anzahl Messungen, Anzahl Materialien, arithmetisches Mittel, Anteil ≥ 80 %, `overfull`-Anteil, letzte Messung.
- Verteilung über alle 449 Standorte: Perzentile und Quartilsbänder; Konzentration der `overfull`-Messungen auf die Standortquartile.
- Top 20 / Bottom 20 nach Standortmittel; Sensitivität ohne Standorte mit < 10 Messungen (41 Standorte).
- **Material-Mix-Kontrolle:** erwarteter Standortwert = mit den Messzahlen gewichtetes Mittel der globalen Materialmittel; Residuum = beobachtet − erwartet; Rangvergleich roh vs. bereinigt.
- **Stabilität:** zwei Halbjahre (2025-10-17–2026-04-09: 5.087 Messungen; 2026-04-10–2026-09-30: 6.614), Spearman-ρ der Standortmittel bei Mindestmessungen 1/2/3/5/8 je Halbjahr, Spearman-Brown-Hochrechnung, beobachtete vs. aus Messrauschen erwartete Streuung der Halbjahresdifferenz, Quintilswechsel.
- **Varianzzerlegung:** einfaktorielle ANOVA über `Location_id` (SSB/SSW, F, η²) sowie OLS mit Dummy-Variablen für Material, Standort und beide (`numpy.linalg.lstsq`).
- Werkzeug: `python3`, pandas 3.0.3, numpy. scipy ist in der Umgebung nicht installiert; der p-Wert der ANOVA stammt aus einer χ²-Näherung.

## Ergebnisse

**Tabelle 1 – Verteilung der Standortkennzahlen über alle 449 Standorte**

| Kennzahl | Min | P5 | P10 | P25 | Median | P75 | P90 | P95 | Max | Mittel |
|---|---|---|---|---|---|---|---|---|---|---|
| Ø Füllstand (%) | 25,0 | 44,8 | 50,0 | 57,9 | 64,0 | 70,4 | 75,8 | 79,3 | 110,0 | 63,7 |
| Anteil ≥ 80 % (%) | 0,0 | 14,6 | 20,8 | 31,8 | 42,4 | 51,7 | 59,7 | 64,7 | 100,0 | 41,5 |
| `overfull`-Anteil (%) | 0,0 | 0,0 | 0,0 | 0,0 | 7,4 | 13,6 | 20,0 | 22,2 | 100,0 | 9,2 |
| Messungen je Standort | 1 | 7 | 10 | 16 | 24 | 35 | 45 | 49 | 97 | 26,1 |

21 Standorte liegen im Mittel ≥ 80 %, 44 unter 50 %. Quartilsbänder: schwächstes Viertel (Ø 25,0–57,9 %, 114 Standorte) mit 23,5 % Messungen ≥ 80 % und 3,8 % `overfull`; stärkstes Viertel (Ø 70,6–110,0 %, 112 Standorte) mit 58,5 % und 16,3 %. Der Median-Standort liegt bei 64,0 % – also fast genau auf dem Grün-Niveau (68,1 %) und deutlich unter Weiß (82,2 %).

**Tabelle 2 – Top 20 Standorte nach mittlerem Füllstand**

`Location_id` auf 8 Zeichen gekürzt (Präfixe eindeutig), Mat. = Anzahl Materialien am Standort.

| # | Location_id | Mat. | n | Ø % | ≥ 80 % | overfull % | letzte Messung |
|---|---|---|---|---|---|---|---|
| 1 | `2e222be0` | 3 | 3 | 110,0 | 100 | 100,0 | 15.05.26 |
| 2 | `f5602e73` | 1 | 1 | 110,0 | 100 | 100,0 | 29.04.26 |
| 3 | `d5be6df1` | 3 | 35 | 91,7 | 80 | 20,0 | 11.09.26 |
| 4 | `83086ae1` | 3 | 40 | 87,8 | 80 | 22,5 | 09.09.26 |
| 5 | `80b7f22a` | 3 | 43 | 87,0 | 70 | 41,9 | 28.09.26 |
| 6 | `c54ed222` | 3 | 6 | 86,7 | 83 | 0,0 | 08.06.26 |
| 7 | `94bc9aca` | 3 | 34 | 85,0 | 68 | 20,6 | 28.08.26 |
| 8 | `df6d6307` | 3 | 42 | 84,0 | 71 | 23,8 | 28.09.26 |
| 9 | `5f14179e` | 3 | 39 | 82,8 | 69 | 25,6 | 21.09.26 |
| 10 | `f019215f` | 3 | 11 | 82,7 | 55 | 27,3 | 25.08.26 |
| 11 | `7d069a27` | 3 | 12 | 82,5 | 75 | 41,7 | 17.08.26 |
| 12 | `c7208f1a` | 3 | 45 | 81,8 | 67 | 20,0 | 09.09.26 |
| 13 | `d9a4e9d2` | 3 | 23 | 81,7 | 65 | 17,4 | 10.07.26 |
| 14 | `3786dd9d` | 3 | 37 | 81,6 | 62 | 18,9 | 28.09.26 |
| 15 | `975d7c3e` | 3 | 10 | 81,0 | 60 | 10,0 | 13.08.26 |
| 16 | `ad21dbbf` | 3 | 21 | 81,0 | 62 | 9,5 | 18.08.26 |
| 17 | `00e9e2cf` | 3 | 48 | 80,8 | 69 | 18,8 | 10.09.26 |
| 18 | `1a342cc5` | 3 | 19 | 80,0 | 58 | 31,6 | 10.09.26 |
| 19 | `06209e37` | 3 | 26 | 80,0 | 65 | 0,0 | 28.08.26 |
| 20 | `61855af3` | 3 | 3 | 80,0 | 33 | 0,0 | 02.02.26 |

Die Ränge 1 und 2 stehen auf 1 bzw. 3 Messungen, die ausnahmslos `overfull` waren – das ist kein Standortvergleich. Ohne Standorte mit < 10 Messungen führt `d5be6df1` mit 91,7 % (35 Messungen), gefolgt von `83086ae1` (87,8 %) und `80b7f22a` (87,0 %); im Mittel ≥ 80 % liegen dann noch 16 der 449 Standorte.

**Tabelle 3 – Bottom 20 Standorte nach mittlerem Füllstand**

| # | Location_id | Mat. | n | Ø % | ≥ 80 % | overfull % | letzte Messung |
|---|---|---|---|---|---|---|---|
| 1 | `b13d8ab0` | 2 | 2 | 25,0 | 0 | 0,0 | 17.06.26 |
| 2 | `4e2ca848` | 3 | 4 | 30,0 | 0 | 0,0 | 19.02.26 |
| 3 | `79d39648` | 3 | 9 | 34,4 | 0 | 0,0 | 28.09.26 |
| 4 | `c397fd5c` | 3 | 11 | 34,5 | 9 | 9,1 | 29.09.26 |
| 5 | `37a212db` | 3 | 19 | 36,3 | 11 | 5,3 | 26.08.26 |
| 6 | `43ff3a23` | 3 | 9 | 36,7 | 0 | 0,0 | 29.07.26 |
| 7 | `36af8e94` | 3 | 16 | 36,9 | 6 | 6,2 | 31.08.26 |
| 8 | `fbe1b4ea` | 2 | 4 | 37,5 | 0 | 0,0 | 08.06.26 |
| 9 | `53a56d2e` | 2 | 2 | 40,0 | 0 | 0,0 | 09.06.26 |
| 10 | `b41eb3e8` | 2 | 6 | 40,0 | 33 | 0,0 | 31.08.26 |
| 11 | `a4cbda51` | 3 | 15 | 40,7 | 13 | 0,0 | 14.09.26 |
| 12 | `a98860e7` | 3 | 11 | 40,9 | 18 | 0,0 | 17.07.26 |
| 13 | `a23183c0` | 3 | 21 | 41,0 | 24 | 0,0 | 14.09.26 |
| 14 | `1a774ebc` | 3 | 17 | 41,2 | 18 | 5,9 | 28.09.26 |
| 15 | `4c52d626` | 3 | 18 | 41,7 | 17 | 0,0 | 13.08.26 |
| 16 | `bdcbc51b` | 3 | 17 | 41,8 | 18 | 5,9 | 27.08.26 |
| 17 | `8fd6c6d5` | 3 | 13 | 42,3 | 15 | 0,0 | 31.08.26 |
| 18 | `d0d9ae07` | 3 | 14 | 42,9 | 7 | 7,1 | 12.08.26 |
| 19 | `1e25f5f5` | 3 | 9 | 43,3 | 0 | 0,0 | 27.08.26 |
| 20 | `59d6d32e` | 3 | 12 | 44,2 | 17 | 0,0 | 15.06.26 |

Auch hier stehen fünf Standorte mit < 10 Messungen in der Liste. Ohne diese führt `c397fd5c` (34,5 %, 11 Messungen) die schwächsten, danach `37a212db` (36,3 %) und `36af8e94` (36,9 %). Auffällig: Die gesamten Bottom 20 liegen unter 45 % – also unter dem Niveau, das Braunglas im Mittel ohnehin erreicht (40,0 %). Dort ist nicht nur ein Material, sondern der ganze Standort schwach ausgelastet.

**Tabelle 4 – Stabilität der Standortmittel zwischen den beiden Halbjahren**

| Mindestmessungen je Halbjahr | Standorte | Pearson r | Spearman ρ | SD der Differenz (pp) |
|---|---|---|---|---|
| 1 | 425 | 0,253 | 0,271 | 15,3 |
| 2 | 420 | 0,258 | 0,274 | 15,1 |
| 3 | 404 | 0,294 | 0,297 | 14,2 |
| 5 | 362 | 0,334 | 0,320 | 13,0 |
| 8 | 284 | 0,323 | 0,295 | 11,9 |

Mittleres Niveau: 69,1 % im ersten vs. 63,5 % im zweiten Halbjahr (−5,6 pp; auf dem Panel der 404 Standorte −5,1 pp). Von den Top 20 des ersten Halbjahres stehen nur 3 im zweiten wieder in den Top 20, von den Bottom 20 ebenfalls 3; 26,5 % der Standorte bleiben im gleichen Quintil, 61,9 % im gleichen oder benachbarten. Die beobachtete SD der Differenz (14,2 pp) liegt nur wenig über der aus reinem Messrauschen erwarteten (12,9 pp bei median 11 Messungen je Halbjahr); der standortspezifische Anteil echter Veränderung liegt damit bei etwa 6 pp. Auf die volle Messreihe hochgerechnet (Spearman-Brown) ergibt sich ρ ≈ 0,46.

**Tabelle 5 – Varianzzerlegung der 11.701 Messwerte**

| Quelle | Anteil an der Gesamtvarianz |
|---|---|
| Standort (`Location_id`), allein | 8,6 % |
| Material, allein | 28,7 % |
| Standort + Material (additiv) | 37,9 % |
| Rest: Messzeitpunkt, Behälterdynamik, 10-pp-Raster | 62,1 % |

ANOVA über `Location_id`: F(448; 11.252) = 2,35, p ≈ 1·10⁻⁵⁰ (χ²-Näherung). Streuung zwischen den Standortmitteln 10,7 pp, mittlere Streuung innerhalb eines Standorts 30,1 pp (Median der Reihen-SD je Material 24,1 pp); die Materialmittel streuen mit 17,5 pp fast doppelt so stark wie die Standortmittel. Die Material-Mix-Kontrolle ändert fast nichts: das bereinigte Standortmittel korreliert mit ρ = 0,986 mit dem rohen (441 der 449 Standorte haben alle drei Materialien) – die Rangliste ist kein Artefakt der Materialzusammensetzung.

## Interpretation

- **Der Standort ist ein Niveauversatz, kein Schicksal.** 10,7 pp Streuung zwischen den Standortmitteln stehen 30,1 pp Streuung innerhalb desselben Standorts gegenüber. Eine Einzelmessung sagt fast nichts über den Standort; erst rund zehn Messungen trennen ein starkes von einem schwachen Niveau.
- **Material schlägt Standort um Faktor 3,3** (28,7 % vs. 8,6 % Varianzanteil). Wer nach Material (Weiß) disponiert, gewinnt mehr als wer nach Standort priorisiert; die 25,8 pp zwischen P10 und P90 der Standorte sind kleiner als der Abstand Braun–Weiß (42,4 pp).
- **Die Rangfolge ist nur schwach reproduzierbar** (ρ = 0,30, hochgerechnet 0,46). Statische Top-Listen sind keine Planungsgrundlage: Halbjahr für Halbjahr verschiebt sich das Niveau um 5,1–5,6 pp, also rund eine halbe Standort-Standardabweichung, und nur jeder vierte Standort bleibt im gleichen Quintil.
- **Trotzdem ist die Konzentration nutzbar:** Die 113 Standorte im stärksten Quartil (Ø ≥ 70,4 %) tragen 48,4 % aller 1.192 `overfull`-Messungen bei 32 % der Messungen, das schwächste Quartil 6,8 %. 21 Standorte liegen im Mittel ≥ 80 %, 46 haben einen `overfull`-Anteil ≥ 20 %, 176 einen ≥ 10 %.
- **Messhäufigkeit ist der wichtigste Störfaktor:** Die Messzahl korreliert mit dem Standortmittel (Spearman ρ = 0,47). Starke Standorte werden häufiger angefahren und häufiger gemessen; ohne Leerungsdaten ist nicht trennbar, ob sie voller sind, weil sie stärker genutzt werden, oder weil sie öfter in die Stichprobe fallen.
- **Datenaktualität ist ungleich:** 403 der 449 Standorte wurden zuletzt im August oder September 2026 gemessen, 46 davor, 10 vor Juni 2026. Für diese 46 steht die Rangfolge auf alten Werten.

## Grenzen

- `overfull` ist als 110 % kodiert, die tatsächliche Höhe ist unbekannt; zusammen mit der 10-pp-Rasterung (nur 12 mögliche Stufen) wird ein Teil der Within-Streuung von 30,1 pp künstlich erzeugt. Die echte Behälterdynamik ist kleiner, die Standortanteile sind entsprechend unscharf.
- 41 Standorte haben < 10 Messungen (12 weniger als 5, einer genau 1). Ihre Mittelwerte sind nicht belastbar, stehen aber in den Tabellen, weil die Aufgabe alle 449 Standorte umfasst; die Sensitivitätsläufe sind im Text genannt.
- Der Halbjahres-Schnitt (2026-04-10) ist willkürlich; jede Hälfte enthält nur die halbe Messreihe, was die Rangkorrelation systematisch nach unten zieht (deshalb die Spearman-Brown-Hochrechnung). Die Rangkorrelation ist eine Untergrenze der Stabilität, kein direkter Beweis für Instabilität.
- F-Test und η² setzen unabhängige Beobachtungen voraus; Messungen desselben Standorts sind zeitlich korreliert. Die Zerlegung 8,6 % / 28,7 % / 37,9 % ist beschreibend, kein Kausalmodell.
- Standortmittel sind durch die jeweils gemessene Teilmenge und den Messzeitpunkt verzerrt; wer im Winter gemessen wurde, sieht andere Werte als wer im Sommer gemessen wurde. Das ist mit 46 Standorten ohne Messung seit August 2026 und dem Halbjahresversatz von 5,6 pp sichtbar.
- Es fehlen Leerungsereignisse, Gefäßgrößen, Adressen (Koordinaten sind synthetische Platzhalter) und Wetter. Damit sind keine räumlichen Cluster, keine Füllmengen in Litern und keine Tourenkosten prüfbar; „starker Standort“ bleibt eine Aussage über Prozentwerte, nicht über Mengen.

## Nächster Schritt

Die negativen Sprünge je Standort-/Material-Reihe als Leerungsindikator zählen und das Standortmittel um die Zeit seit der letzten erkennbaren Leerung bereinigen; erst wenn der Rang danach stabil bleibt (ρ > 0,7 zwischen den Halbjahren), ist der Standort eine planbare Größe und nicht nur ein Zeitpunktartefakt.
