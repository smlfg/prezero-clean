# 07 – Materialabhängige Schwellenwerte

> Ein einheitlicher 80-%-Schwellwert ist nur für Weißglas richtig: Weiß braucht 80 %, Grün 70 % und Braun 60 % – weil nach einer Braun-Messung bei 80 % die übernächste Messung nur in 5,8 % der Fälle ein Überlauf ist, während dieselbe Situation bei Weiß in 19,9 % der Fälle überläuft.

## Frage

Welcher Warnschwellwert (in Prozent Füllstand) ist je Material operativ sinnvoll, wenn das Ziel „kein Überlauf vor der nächsten Leerung" gilt? Und was kostet ein einheitlicher 80-%-Schwellwert im Vergleich?

## Vorgehen

- Datengrundlage: `../glass_fill_levels_anonymized_f.csv`, 11.701 Messungen, 1.338 Standort-/Material-Zeitreihen (Braun 442, Grün 448, Weiß 448). `overfull` als 110 % kodiert (tatsächliche Höhe unbekannt).
- **Tabelle 1:** kumulierte Verteilung aller Messungen je Material (Anteil ≥ x, x = 40…100, plus `overfull`).
- **Tabelle 2/3:** Übergänge innerhalb einer Zeitreihe (n = 10.363, chronologisch sortiert): P(Folgemessung ≥ 80 % | aktuelle Messung = x) und P(Folgemessung `overfull` | aktuelle Messung = x), je Material, mit Fallzahl.
- **Kriterium für die Schwelle** – drei Bedingungen, jede Zahl muss eine davon tragen:
  1. *Physik (Headroom):* Schwelle = 80 % minus erwarteter Zuwachs bis zur nächsten Messung (medianer Zuwachs/30 Tage × medianes Intervall, nur Anstiege).
  2. *Signal (Elbow):* Stufe, ab der die Überlaufwahrscheinlichkeit der Folgemessung springt und nicht mehr auf dem Niveau des leeren Behälters liegt.
  3. *Blindfleck:* Anteil der `overfull`-Messungen, deren Vorgängermessung **unter** der Schwelle lag (Überlauf ohne Vorwarnung).
  Zusätzlich als Kostenmaß: Alarmrate (Anteil aller Übergänge ≥ Schwelle), Alarme je Zeitreihe, Abdeckung (Anteil aller kritischen Folgemessungen, die die Schwelle fängt).
- „Kritisch" = Folgemessung ≥ 80 %. „Fehlalarm" = Folgemessung < 80 %; davon wird der Anteil ausgewiesen, der ein Rückgang (Leerung) ist.
- Werkzeug: `python3` mit pandas.

## Ergebnisse

**Tabelle 1 – Kumulierte Verteilung aller Messungen (Anteil ≥ x in %)**

| Material | n | ≥ 40 | ≥ 50 | ≥ 60 | ≥ 70 | ≥ 80 | ≥ 90 | ≥ 100 | overfull |
|---|---|---|---|---|---|---|---|---|---|
| Braun | 3.100 | 41,6 | 30,1 | 24,5 | 18,8 | 14,7 | 11,4 | 7,9 | 3,4 |
| Grün | 4.169 | 85,3 | 74,1 | 64,0 | 52,4 | 43,8 | 33,6 | 24,7 | 8,6 |
| Weiß | 4.432 | 95,2 | 90,9 | 84,9 | 75,2 | 66,4 | 53,2 | 42,2 | 16,5 |

Die drei Verteilungen sind fast gegeneinander verschoben, nicht unterschiedlich geformt: Weiß liegt bei jeder Stufe um 50–80 Prozentpunkte über Braun. Ein materialunabhängiger Prozentwert schneidet deshalb drei völlig verschiedene Teilmengen: 80 % sind bei Braun die obersten 15 %, bei Weiß zwei Drittel aller Messungen.

**Tabelle 2 – P(Folgemessung ≥ 80 % | aktuelle Messung = x) in %, mit n**

| x | Braun | Grün | Weiß |
|---|---|---|---|
| 20 | 8,1 (n = 739) | 25,0 (n = 128) | 57,9 (n = 57) |
| 30 | 17,0 (477) | 30,9 (349) | 50,5 (99) |
| 40 | 19,2 (308) | 35,4 (410) | 60,7 (168) |
| 50 | 19,6 (148) | 37,8 (362) | 61,0 (241) |
| 60 | 20,1 (149) | 41,0 (442) | 60,6 (388) |
| 70 | 22,6 (115) | 43,9 (326) | 65,0 (334) |
| 80 | 29,3 (92) | 47,5 (383) | 64,8 (534) |
| 90 | 27,6 (105) | 53,5 (342) | 68,0 (444) |
| 100 | 31,5 (127) | 59,6 (621) | 75,3 (1.026) |
| **Basisrate** | **16,4** | **44,6** | **67,1** |

Der Füllstand ist ein schwacher Prädiktor. Braun steigt von 8 % (bei x = 20) auf 31 % (bei x = 100) – Faktor 4, aber auf niedrigem Niveau. Weiß bewegt sich zwischen 58 % und 75 %, weil ein Weißglasbehälter fast immer voll ist: die Basisrate von 67,1 % dominiert, der Messwert erklärt fast nichts. Nur bei Grün wächst die Kurve monoton und deutlich (25 % → 60 %).

**Tabelle 3 – P(Folgemessung overfull | aktuelle Messung = x) in %**

| x | Braun (Basis 3,7) | Grün (Basis 9,4) | Weiß (Basis 17,8) |
|---|---|---|---|
| 20 | 1,4 (n = 739) | 5,5 (128) | 15,8 (57) |
| 40 | 4,2 (308) | 5,1 (410) | 14,3 (168) |
| 60 | 5,4 (149) | 8,6 (442) | 11,1 (388) |
| 70 | 6,1 (115) | **13,5** (326) | 14,1 (334) |
| 80 | 7,6 (92) | 8,9 (383) | 14,6 (534) |
| 90 | 3,8 (105) | 12,0 (342) | 19,6 (444) |
| 100 | 5,5 (127) | 12,2 (621) | 20,5 (1.026) |

Hier liegt der einzige echte Sprung: Grün verdoppelt sein Überlaufrisiko zwischen 60 % und 70 % (8,6 → 13,5 %); darüber fällt es wieder auf 8,9 % (n = 383, Zufallsbreite). Braun bleibt von 40 % bis 100 % flach zwischen 3,8 % und 7,6 % – der Braun-Überlauf hängt nicht am Füllstand, sondern am Abstand (median 48 Tage zwischen Vorgänger und `overfull`, gegenüber 31–34 Tagen bei Grün/Weiß). Weiß steigt erst ab 90 % klar (19,6/20,5 %).

**Tabelle 4 – Schwellenwerte im Vergleich (Übergänge je Material)**

| Material | T | Alarmrate | Trefferquote | Abdeckung | Fehlalarmrate | P(next overfull │ ≥ T) | Alarme je Reihe |
|---|---|---|---|---|---|---|---|
| Braun | 60 | 25,5 % | 27,0 % | 41,9 % | 73,0 % | 5,7 % | 1,6 |
| Braun | 70 | 19,9 % | 28,9 % | 35,0 % | 71,1 % | 5,8 % | 1,3 |
| Braun | 80 | 15,6 % | 30,6 % | 29,1 % | 69,4 % | 5,8 % | 1,0 |
| Grün | 60 | 65,5 % | 50,2 % | 73,8 % | 49,8 % | 11,6 % | 5,6 |
| Grün | 70 | 53,6 % | 52,3 % | 62,9 % | 47,7 % | 12,2 % | 4,5 |
| Grün | 80 | 44,9 % | 54,0 % | 54,2 % | 46,0 % | 12,0 % | 3,8 |
| Weiß | 70 | 75,7 % | 69,4 % | 78,3 % | 30,6 % | 19,2 % | 6,8 |
| Weiß | 80 | 67,3 % | 70,0 % | 70,2 % | 30,0 % | 19,9 % | 6,1 |
| Weiß | 90 | 53,9 % | 71,2 % | 57,2 % | 28,8 % | 21,2 % | 4,9 |

**Headroom-Rechnung** (medianer Zuwachs je Intervall, nur Anstiege): Braun 17,9 pp/30 d × 33 d = 19,7 pp → Schwelle 60 % für „nächste Messung < 80 %", 80 % für „< 100 %". Grün 27,0 × 27 d = 24,3 pp → 56 % / 76 %. Weiß 22,2 × 27 d = 20,0 pp → 60 % / 80 %. Die drei Zahlen sind fast identisch – der Materialunterschied entsteht nicht aus der Füllgeschwindigkeit, sondern aus dem Niveau und der Leerungshäufigkeit.

**Tabelle 5 – Abgeleitete Schwellen und Differenz zum einheitlichen 80-%-Wert**

| Material | Schwelle | Begründung | Δ Alarme ggü. 80 % | kritisch früher erkannt | Abdeckung (T vs. 80 %) | Blindfleck (T vs. 80 %) |
|---|---|---|---|---|---|---|
| Braun | **60 %** | Headroom exakt 60 %; Überlaufrisiko-Plateau 5,7 % ab 60; Blindfleck sinkt um 15,2 pp | +264 | +56 (median 31 Tage früher) | 41,9 vs. 29,1 % | 60,6 vs. 75,8 % |
| Grün | **70 %** | einziger Elbow (8,6 → 13,5 %); Blindfleck 30,3 vs. 42,9 % | +326 | +143 (median 26 Tage früher) | 62,9 vs. 54,2 % | 30,3 vs. 42,9 % |
| Weiß | **80 %** | unter 80 % kein Signalgewinn, über 80 % steigt der Blindfleck auf 35,7 % | 0 | 0 | 70,2 % | 24,7 % |

Zum Vergleich die verworfenen Alternativen: Braun bei 70 % kostet 115 Alarme und verliert 8,1 pp Blindfleckvorteil; Grün bei 60 % alarmiert 65,5 % aller Übergänge für 10,9 pp mehr Abdeckung; Weiß bei 70 % erzeugt 334 zusätzliche Alarme für 217 zusätzliche Treffer – eine marginale Trefferquote von 65,0 %, also **unter** der Weiß-Basisrate von 67,1 %. Jeder zusätzliche Weiß-Alarm unter 80 % ist damit schlechter als eine Zufallsauswahl.

## Interpretation

- **Braun 60 %:** Braun überläuft selten (3,7 %) und dann nicht wegen des Füllstands, sondern wegen des langen Intervalls. 60 % ist die einzige Zahl, die sowohl die Physik (19,7 pp Zuwachs bis zur nächsten Messung) als auch das Kostenmaß trägt: 1,6 Alarme pro Zeitreihe bei median 6 Messungen. Die Schwelle senkt den Blindfleck von 75,8 % auf 60,6 %, also wird gut ein Fünftel der bisher unangekündigten Braun-Überläufe erstmals vorher sichtbar.
- **Grün 70 %:** Nur hier existiert ein echter Schwellwert. 70 % ist die Stufe, ab der das Überlaufrisiko der Folgemessung von 8,6 % auf 13,5 % springt und ab der 143 kritische Messungen eine Periode (26 Tage) früher auffallen als bei 80 %. Die 53,6 % Alarmrate ist der Preis; unter 70 % kauft jeder weitere Alarm nur Rauschen.
- **Weiß 80 % – aber als Dauerbedingung, nicht als Warnung:** Bei 80 % lösen zwei von drei Übergängen aus, 6,1 Alarme pro Reihe. Das ist keine Ausnahmemeldung, sondern der Normalzustand. Eine Weiß-Schwelle unter 80 % ist mathematisch wertlos, weil der Messwert dort nicht mehr Information trägt als der Materialdurchschnitt.
- **Der einheitliche 80-%-Wert ist nicht falsch, sondern nur für ein Material passend.** Für Braun ist er 15,2 pp zu spät (drei Viertel der Braun-Überläufe kommen ohne Vorwarnung), für Grün 8,7 pp zu spät, für Weiß genau richtig. Die Verschiebung ist nicht symmetrisch: Braun und Grün früher zu warnen kostet 590 zusätzliche Alarme und fängt 199 zusätzliche kritische Messungen.
- **„Fehlalarme" sind fast immer Leerungen.** Bei T = 80 besteht jeder nicht-kritische Folgefall aus einem Rückgang (100 %), bei T = 70/60 sind es 95–97 %; nur 25 (Braun, 60 %), 28 (Grün, 70 %) Fälle bleiben „mittig stehen". Die Fehlalarmrate misst also überwiegend, wie oft zwischen zwei Messungen geleert wurde – nicht, wie oft die Prognose falsch war. Das ist die entscheidende Einschränkung jeder Schwellenoptimierung auf diesen Daten.

## Grenzen

- **Keine Leerungsereignisse:** Ein negativer Sprung ist nur ein Indiz für Leerung, kein Beweis. „Fehlalarm" und „Überlauf vor der nächsten Leerung" sind deshalb nicht exakt trennbar; die Fehlalarmraten sind Obergrenzen.
- **`overfull` = 110 % kodiert**, tatsächliche Höhe unbekannt; Überlaufwahrscheinlichkeiten sind eher unterschätzt, weil ein Behälter nur einmal als `overfull` gezählt wird, egal wie lange er überläuft.
- **Kleine Fallzahlen bei Braun:** 115 Übergänge bei exakt 70 %, 92 bei 80 %, 99 `overfull`-Messungen mit Vorgänger. Die Braun-Kurve ist in Tabelle 3 zwischen 40 % und 100 % statistisch nicht von flach unterscheidbar; die 60-%-Empfehlung stützt sich auf Headroom und Blindfleck, nicht auf einen signifikanten Sprung.
- **Selektive Messung:** Messhäufigkeit korreliert mit dem Niveau (häufiger angefahrene Standorte sind voller). P(next ≥ 80 %) ist daher für viel gemessene Zeitreihen überschätzt; Braun hat mit 33 Tagen den größten Messabstand und damit den größten Extrapolationsfehler.
- **10-pp-Raster:** Schwellen zwischen den Stufen (etwa 65 % oder 75 %) sind nicht prüfbar; die Empfehlung ist auf die Rasterpunkte beschränkt.
- Der Vergleich setzt voraus, dass jede Warnung in eine Leerung mündet. Tatsächliche Fahrzeugkapazität, Tourenlänge und Anfahrtskosten fehlen – die Alarmrate ist nur ein Stellvertreter für Kosten.

## Nächster Schritt

Die 679 Braun-Übergänge ≥ 60 % gegen die 415 Übergänge ≥ 80 % auf Standortebene schneiden und prüfen, ob die 56 zusätzlich früher erkannten Fälle an weniger als 50 Standorten liegen – dann ist die 60-%-Schwelle als kurze Zusatzrunde für diese Standorte fahrbar, ohne die Gesamttour zu verlängern.
