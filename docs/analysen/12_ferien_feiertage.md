# 12 – Ferien- und Feiertagseffekte

> Kein Ferienfenster weicht mehr als 7 Prozentpunkte vom Monatsmittel derselben Zeit ab (Ausnahme Ostern-Braun mit n = 15); die Monatsmittel selbst schwanken 2025/26 um 31,5 pp – ein Ferieneffekt ist in diesen Daten nicht vom Saison-, Trend- und Abdeckungseffekt trennbar.

## Frage

Unterscheiden sich die Füllstände 14 Tage vor, während und 14 Tage nach Weihnachten, Ostern, Pfingsten und den Sommerferien – und bleibt ein Unterschied bestehen, wenn man ihn gegen das Monatsmittel derselben Zeit statt gegen die Nachbarwoche prüft?

## Vorgehen

- Datengrundlage: `../glass_fill_levels_anonymized_f.csv`, 11.701 Messungen, 229 Messtage in 349 Kalendertagen (2025-10-17 bis 2026-09-30). `overfull` als 110 % kodiert (tatsächliche Höhe unbekannt). 10-pp-Raster.
- **Fensterdefinition, geprüft** gegen die Termine des Kultusministeriums BW (km.baden-wuerttemberg.de, schulferien.org):
  - Weihnachtsferien **22.12.2025–05.01.2026** (15 Tage) – bestätigt.
  - Osterferien offiziell 30.03.–**11.04.2026**; verwendet **30.03.–10.04.2026** (12 Tage). Annahme: der 11.04. ist ein Samstag, und Samstage tragen nur 3,8 % der Messungen (444 von 11.701) – der eine Tag ändert kein Segmentergebnis.
  - Pfingstferien **26.05.–05.06.2026** (11 Tage) – bestätigt.
  - Sommerferien **30.07.–12.09.2026** (45 Tage) – bestätigt.
- Segmente je Fenster: **15 Kalendertage davor** (Start − 15 bis Start − 1), **Fenster**, **14 Kalendertage danach** (Ende + 1 bis Ende + 14).
- Kennzahlen je Segment × Material: Messtage, n, Mittelwert, Anteil ≥ 80 %, `overfull`-Anteil. Leseregel: Segmente mit **n < 50** sind als nicht interpretierbar mit `*` markiert.
- **Zusatzcheck A:** Fenstermittel gegen das tagesgewichtete Mittel der berührten Kalendermonate (Saison-Referenz statt Nachbarwoche).
- **Zusatzcheck B:** balanciertes Dreier-Panel – nur Zeitreihen (`Location_id` × `material_type`), die in allen drei Segmenten eines Fensters messen; damit fällt der Standortwechsel als Störgröße weg.
- **Feiertage:** alle 11 gesetzlichen Feiertage in BW im Zeitraum einzeln auf Messungen geprüft.
- Werkzeug: `python3` mit pandas.

## Ergebnisse

**Tabelle 1 – Abdeckung der Segmente**

| Ferien | Fenster | Tage | Messtage vor/Fenster/nach | n vor/Fenster/nach | n je Kalendertag vor/Fenster/nach |
|---|---|---:|---|---|---|
| Weihnachten | 2025-12-22–2026-01-05 | 15 | 13 / 11 / 6 | 674 / 516 / 154 | 44,9 / 34,4 / 11,0 |
| Ostern | 2026-03-30–2026-04-10 | 12 | 11 / 6 / 10 | 277 / 194 / 452 | 18,5 / 16,2 / 32,3 |
| Pfingsten | 2026-05-26–2026-06-05 | 11 | 10 / 8 / 11 | 569 / 561 / 818 | 37,9 / 51,0 / 58,4 |
| Sommer | 2026-07-30–2026-09-12 | 45 | 11 / 30 / 6 | 678 / 1.698 / 330 | 45,2 / 37,7 / 23,6 |

Die Segmente sind unterschiedlich dicht besetzt: zwischen 11,0 und 58,4 Messungen je Kalendertag. `*` = n < 50, nicht interpretiert.

**Tabelle 2 – Kennzahlen je Segment und Material**

| Ferien | Segment | Material | Messtage | n | Ø % | ≥ 80 % | overfull % |
|---|---|---|---:|---:|---:|---:|---:|
| Weihnachten | 14 davor | Braun | 13 | 222 | 28,4 | 5,4 | 0,0 |
| Weihnachten | 14 davor | Grün | 13 | 226 | 70,1 | 46,5 | 0,9 |
| Weihnachten | 14 davor | Weiß | 13 | 226 | 83,6 | 71,7 | 0,9 |
| Weihnachten | Fenster | Braun | 11 | 172 | 31,7 | 3,5 | 0,0 |
| Weihnachten | Fenster | Grün | 11 | 172 | 70,1 | 43,0 | 0,0 |
| Weihnachten | Fenster | Weiß | 11 | 172 | 82,9 | 74,4 | 0,6 |
| Weihnachten | 14 danach | Braun | 4 | 19* | 72,1 | 42,1 | 36,8 |
| Weihnachten | 14 danach | Grün | 6 | 63 | 87,5 | 68,3 | 46,0 |
| Weihnachten | 14 danach | Weiß | 6 | 72 | 92,6 | 73,6 | 50,0 |
| Ostern | 14 davor | Braun | 8 | 24* | 78,8 | 58,3 | 45,8 |
| Ostern | 14 davor | Grün | 11 | 91 | 78,9 | 56,0 | 24,2 |
| Ostern | 14 davor | Weiß | 11 | 162 | 83,5 | 63,6 | 28,4 |
| Ostern | Fenster | Braun | 3 | 15* | 82,7 | 73,3 | 33,3 |
| Ostern | Fenster | Grün | 5 | 70 | 74,1 | 52,9 | 17,1 |
| Ostern | Fenster | Weiß | 6 | 109 | 86,6 | 68,8 | 42,2 |
| Ostern | 14 danach | Braun | 9 | 122 | 67,0 | 50,0 | 4,9 |
| Ostern | 14 danach | Grün | 10 | 157 | 84,1 | 73,9 | 17,8 |
| Ostern | 14 danach | Weiß | 10 | 173 | 93,0 | 83,8 | 29,5 |
| Pfingsten | 14 davor | Braun | 10 | 190 | 56,0 | 30,0 | 13,2 |
| Pfingsten | 14 davor | Grün | 10 | 189 | 76,3 | 56,1 | 21,2 |
| Pfingsten | 14 davor | Weiß | 10 | 190 | 90,6 | 81,6 | 31,6 |
| Pfingsten | Fenster | Braun | 6 | 77 | 37,1 | 9,1 | 2,6 |
| Pfingsten | Fenster | Grün | 8 | 240 | 67,5 | 38,8 | 13,3 |
| Pfingsten | Fenster | Weiß | 8 | 244 | 80,5 | 60,2 | 23,0 |
| Pfingsten | 14 danach | Braun | 7 | 133 | 27,8 | 5,3 | 0,0 |
| Pfingsten | 14 danach | Grün | 11 | 340 | 45,6 | 10,9 | 0,6 |
| Pfingsten | 14 danach | Weiß | 11 | 345 | 60,0 | 28,1 | 5,8 |
| Sommer | 14 davor | Braun | 11 | 217 | 36,7 | 8,8 | 0,5 |
| Sommer | 14 davor | Grün | 11 | 231 | 67,1 | 44,2 | 3,9 |
| Sommer | 14 davor | Weiß | 11 | 230 | 83,6 | 73,5 | 13,0 |
| Sommer | Fenster | Braun | 27 | 473 | 32,3 | 6,8 | 0,2 |
| Sommer | Fenster | Grün | 30 | 605 | 60,0 | 31,6 | 2,3 |
| Sommer | Fenster | Weiß | 30 | 620 | 78,2 | 62,3 | 6,8 |
| Sommer | 14 danach | Braun | 6 | 110 | 36,3 | 10,0 | 0,0 |
| Sommer | 14 danach | Grün | 6 | 110 | 64,5 | 40,0 | 1,8 |
| Sommer | 14 danach | Weiß | 6 | 110 | 86,2 | 71,8 | 9,1 |

Gesamtmittel je Monat (alle Materialien): Okt 55,6 · Nov 59,5 · Dez 62,9 · Jan 76,1 · Feb 76,5 · Mär 85,2 · Apr 82,3 · Mai 74,4 · Jun 53,7 · Jul 61,4 · Aug 57,5 · Sep 64,1 – Spannweite 31,5 pp.

**Tabelle 3 – Zusatzcheck A: Fenster gegen Monatsmittel**

| Ferien | Material | Ø Fenster % | Ø Monat(e) % | Δ pp | Δ relativ |
|---|---|---:|---:|---:|---:|
| Weihnachten | Braun | 31,7 | 36,5 | −4,7 | −13 % |
| Weihnachten | Grün | 70,1 | 76,4 | −6,2 | −8 % |
| Weihnachten | Weiß | 82,9 | 87,2 | −4,3 | −5 % |
| Ostern | Braun | 82,7 | 66,7 | +16,0 | +24 % |
| Ostern | Grün | 74,1 | 81,3 | −7,2 | −9 % |
| Ostern | Weiß | 86,6 | 91,8 | −5,2 | −6 % |
| Pfingsten | Braun | 37,1 | 45,2 | −8,1 | −18 % |
| Pfingsten | Grün | 67,5 | 64,1 | +3,4 | +5 % |
| Pfingsten | Weiß | 80,5 | 77,2 | +3,2 | +4 % |
| Sommer | Braun | 32,3 | 33,9 | −1,6 | −5 % |
| Sommer | Grün | 60,0 | 60,4 | −0,3 | −1 % |
| Sommer | Weiß | 78,2 | 78,8 | −0,6 | −1 % |

**Tabelle 4 – Zusatzcheck B: balanciertes Dreier-Panel (gleiche Zeitreihen in allen drei Segmenten)**

| Ferien | Trio-Serien | Material | 14 davor | Fenster | 14 danach |
|---|---:|---|---:|---:|---:|
| Weihnachten | 52 | Braun | 32,0 (n = 5) | 30,0 (n = 4) | 72,5 (n = 4) |
| Weihnachten | 52 | Grün | 72,6 (n = 27) | 71,3 (n = 30) | 80,9 (n = 23) |
| Weihnachten | 52 | Weiß | 84,1 (n = 29) | 85,6 (n = 32) | 89,6 (n = 25) |
| Ostern | 7 | Braun | – (n = 0) | – | – |
| Ostern | 7 | Grün | 80,0 (n = 4) | 66,7 (n = 3) | 70,0 (n = 3) |
| Ostern | 7 | Weiß | 102,0 (n = 5) | 86,0 (n = 5) | 98,0 (n = 5) |
| Pfingsten | 117 | Braun | 60,0 (n = 10) | 42,0 (n = 10) | 18,0 (n = 10) |
| Pfingsten | 117 | Grün | 82,8 (n = 54) | 67,1 (n = 56) | 41,9 (n = 72) |
| Pfingsten | 117 | Weiß | 96,9 (n = 55) | 80,7 (n = 56) | 58,9 (n = 74) |
| Sommer | 197 | Braun | 39,2 (n = 63) | 29,4 (n = 87) | 37,4 (n = 61) |
| Sommer | 197 | Grün | 71,0 (n = 69) | 56,9 (n = 122) | 66,9 (n = 67) |
| Sommer | 197 | Weiß | 89,9 (n = 71) | 79,3 (n = 123) | 87,7 (n = 69) |

Ostern fällt im Panel aus (nur 7 Serien). Pfingsten und Sommer sind die einzigen Fenster mit belastbarem Panel.

**Feiertage:** Alle 11 gesetzlichen Feiertage in BW im Zeitraum (01.11.2025, 25./26.12.2025, 01.01., 06.01., 03.04., 06.04., 01.05., 14.05., 25.05., 04.06.2026) haben **exakt 0 Messungen**. An den beiden Halbtagen mit Betrieb liegt 24.12. bei 39 Messungen (Ø 47,9 %) und 31.12. bei 66 (Ø 67,3 %; Tagesmedian im Datensatz: 51).

## Interpretation

- **Der Nachbarvergleich misst den Trend, nicht die Ferien.** Weihnachten springt von 61,6 % (Fenster, alle Materialien) auf 88,0 % in den 14 Tagen danach – das sind +26,4 pp und wirkt wie ein Ferieneffekt. Es ist der Jahresanstieg: Monatsmittel Dezember 62,9 % → Januar 76,1 % (+13,2 pp). Zusätzlich hat das Segment „danach“ nur 6 Messtage und 11,0 Messungen je Kalendertag statt 44,9 davor.
- **Dünn gemessene Tage liegen systematisch höher.** Rangkorrelation zwischen Tages-n und Tagesmittel: −0,33. 23 Tage mit n < 20 haben im Mittel 73,7 %, 206 Tage mit n ≥ 20 dagegen 67,2 %. Genau die dünnen Segmente (Weihnachten danach, Ostern davor, Ostern Fenster) tragen also einen Aufwärtsbias – dort sind auch fast alle `*`-Werte.
- **Gegen das Monatsmittel bleibt fast nichts übrig.** Interpretierbare Abweichungen: Weihnachten −4,3 bis −6,2 pp, Ostern −5,2 bis −7,2 pp, Pfingsten +3,2/+3,4 pp (Braun −8,1), Sommer −0,3 bis −1,6 pp. Ostern-Braun mit +16,0 pp beruht auf 15 Messungen an 3 Tagen und wird nicht interpretiert. Zum Vergleich: allein die Monatsmittel bewegen sich um 31,5 pp.
- **Pfingsten ist der Juni-Einbruch, nicht die Ferien.** Im Panel (117 Serien) fällt Weiß 96,9 → 80,7 → 58,9 %, Braun 60,0 → 42,0 → 18,0 %. Der Rückgang setzt nach dem Ferienende verstärkt fort; Juni 2026 ist mit 53,7 % der Jahrestiefstwert. Das Muster passt zu einem saisonalen Trog, nicht zu zwei Ferienwochen.
- **Sommer zeigt den einzigen konsistenten Rückgang innerhalb der Ferien.** Panel (197 Serien): Weiß 89,9 → 79,3 → 87,7 %, Grün 71,0 → 56,9 → 66,9 % – Absenkung während der 45 Ferientage, Erholung danach. Gleichzeitig ist das der August-Trog (Jul 61,4 %, Aug 57,5 %, Sep 64,1 %), und relativ zum Monatsmittel sind es nur −0,3 bis −1,6 pp. Urlaubsabwesenheit, Hitze, Leerungsturnus und Meldeverhalten sind hier nicht trennbar.
- **Feiertage erzeugen ein Messloch, kein Niveau.** Über Weihnachten fehlen 25./26.12. und 01.01./06.01., über Ostern Karfreitag und Ostermontag. Der Abstand zwischen zwei Messungen wächst dadurch, was den Füllstand danach mechanisch hebt. Ob die Leerung ausfiel oder nur nicht erfasst wurde, sagt der Datensatz nicht.

## Grenzen

- **Kein Leerungsdatum.** Der Füllstand ist Funktion von Zeit seit letzter Leerung und Zulauf; Ferien können beide verändern. Ohne Leerungsereignisse sind Saison-, Ferien- und Leerungseffekt nicht trennbar – alle Aussagen hier sind deskriptiv.
- **Ein Jahr, jede Ferien einmal.** Keine Wiederholung, keine zweite Sommerpause im Datensatz; Signifikanztests wären bei n = 1 Saison pro Fenster nicht belastbar und werden nicht berichtet.
- **Abdeckung schwankt stark:** 3 bis 127 Messungen je Tag (Median 51); Segmente zwischen 11,0 und 58,4 je Kalendertag. 120 der 349 Kalendertage haben keine Messung, davon 44 Sonntage und 39 Samstage.
- **Segmentzusammensetzung wechselt:** typischer Messabstand ≈ 41 Tage, deshalb messen in einem 14-Tage-Segment überwiegend andere Standorte als im Nachbarsegment. Nur 52 (Weihnachten), 117 (Pfingsten) und 197 (Sommer) Serien liegen in allen drei Segmenten; Ostern mit 7 Serien ist nicht prüfbar.
- **Kein Wochenendbetrieb:** Samstag 3,8 %, Sonntag 0,2 % der Messungen. Ein Ferienwochenend-Effekt ist mit diesen Daten grundsätzlich nicht messbar.
- Aggregate über Messtage sind durch die jeweils gemessene Teilmenge verzerrt; `overfull` ist als 110 % kodiert, die tatsächliche Höhe ist unbekannt; die 10-pp-Rasterung begrenzt die Auflösung; `Location_id` bezeichnet einen Standort, nicht einen einzelnen Behälter.

## Nächster Schritt

Leerungsereignisse (Datum, Standort, Material, Menge) für 2025-10 bis 2026-09 beschaffen und jeden Füllstand auf „Tage seit letzter Leerung“ normieren – erst damit lässt sich der Sommerrückgang im Panel (Weiß 89,9 → 79,3 %) von einem verlängerten Leerungsintervall in den Ferien trennen.
