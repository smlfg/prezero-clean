# 14 – Sommer- und Urlaubsperioden

> Während der Sommerferien liegen die Füllstände an denselben Standorten **1,3 bis 2,3 pp höher** als vom 01.06. bis 29.07. – der Sommertiefpunkt ist der Juni (53,7 %), acht Wochen vor Ferienbeginn; eine pauschale Intervallverlängerung ist damit nicht belegt, differenziert nur für 144 von 440 Zeitreihen (33 %), überwiegend Braun.

## Frage

Sind die Füllstände während der Sommerferien niedriger – und reicht ein solcher Rückgang aus, um Routen und Leerungsintervalle temporär anzupassen?

## Vorgehen

- Datengrundlage: `../glass_fill_levels_anonymized_f.csv`, gefiltert auf 2026-06-01 bis 2026-09-30 (4.884 der 11.701 Messungen). `overfull` als 110 % kodiert (tatsächliche Höhe unbekannt). 10-pp-Raster.
- **Ferienfenster (Annahme, dokumentiert):** 30.07.–12.09.2026 = 45 Kalendertage. Die Termine sind aus der Aufgabenstellung übernommen und deckungsgleich mit der Prüfung gegen das Kultusministerium BW in Analyse 12. Annahme: das Fenster gilt stadtweit und materialunabhängig; Ferienbeginn und -ende sind keine messbaren Ereignisse im Datensatz.
- Vergleichszeiträume: **davor** 01.06.–29.07. (59 Tage; enthält den Pfingstferien-Rest 01.–05.06.), **Ferien** 30.07.–12.09. (45 Tage), **danach** 13.09.–30.09. (18 Tage).
- Kennzahlen je Periode × Material: Messtage, n, Mittelwert, Median, Anteil ≥ 80 %, `overfull`-Anteil.
- **Kontrolle 1 – balanciertes Panel:** nur Zeitreihen (`Location_id` × `material_type`), die in beiden Vergleichszeiträumen messen (Panel A, davor + Ferien) bzw. in allen drei (Panel B). Damit fällt der Standortwechsel als Störgröße weg.
- **Kontrolle 2 – standortzentriert:** je Zeitreihe wird das Mittel über 01.06.–30.09. abgezogen; berichtet wird die mittlere Abweichung je Periode. Das entfernt das Niveau des Standorts vollständig, auch ohne Panel-Schnitt.
- **Kontrolle 3 – gleiches Gewicht je Standort:** erst Mittelwert je `Location_id`, dann ungewichteter Mittelwert über Standorte.
- **Kontrolle 4 – Kurzfenster und Basisrate:** 14 Tage vor Ferienbeginn (16.–29.07.) gegen die Ferien im Panel; zusätzlich alle 334 rollierenden 14-Tage-Fenster des Datensatzes mit ihrem Delta zum jeweils vorangehenden 14-Tage-Fenster, um einzuordnen, wie ungewöhnlich ein Rückgang zum Ferienstart ist.
- **Zeitreihen-Klassifikation:** nur Serien mit ≥ 2 Messungen in den Ferien (440 von 1.099 gemessenen), damit eine einzelne Messung nicht als Urteil durchgeht.
- Werkzeug: `python3` mit pandas.

## Ergebnisse

**Tabelle 1 – Abdeckung der Perioden**

| Periode | Tage | Messtage | n | Standorte | Zeitreihen | n je Serie | Materialmix W/G/B % |
|---|---:|---:|---:|---:|---:|---:|---|
| davor 01.06.–29.07. | 59 | 41 | 2.685 | 428 | 1.203 | 2,2 | 39,2 / 38,9 / 21,9 |
| Ferien 30.07.–12.09. | 45 | 30 | 1.698 | 389 | 1.099 | 1,5 | 36,5 / 35,6 / 27,9 |
| danach 13.09.–30.09. | 18 | 9 | 501 | 174 | 498 | 1,0 | 34,9 / 34,9 / 30,1 |

Die Ferien sind dünner gemessen (37,7 statt 45,5 Messungen je Kalendertag) und enthalten anteilig 6,0 pp mehr Braun. „Danach“ hat nur 9 Messtage und ist nicht belastbar.

**Tabelle 2 – Kennzahlen je Periode und Material**

| Periode | Material | Messtage | n | Ø % | Median % | ≥ 80 % | overfull % |
|---|---|---:|---:|---:|---:|---:|---:|
| davor | Braun | 34 | 587 | 35,3 | 30 | 9,2 | 1,0 |
| davor | Grün | 41 | 1.045 | 55,5 | 50 | 26,6 | 3,4 |
| davor | Weiß | 41 | 1.053 | 70,6 | 70 | 47,6 | 9,1 |
| davor | **gesamt** | 41 | 2.685 | **57,0** | 50 | **31,0** | 5,1 |
| Ferien | Braun | 27 | 473 | 32,3 | 20 | 6,8 | 0,2 |
| Ferien | Grün | 30 | 605 | 60,0 | 60 | 31,6 | 2,3 |
| Ferien | Weiß | 30 | 620 | 78,2 | 80 | 62,3 | 6,8 |
| Ferien | **gesamt** | 30 | 1.698 | **59,0** | 60 | **35,9** | 3,4 |
| danach | Braun | 9 | 151 | 40,7 | 30 | 13,2 | 6,0 |
| danach | Grün | 9 | 175 | 66,0 | 60 | 41,7 | 13,1 |
| danach | Weiß | 9 | 175 | 85,8 | 100 | 70,3 | 23,4 |
| danach | **gesamt** | 9 | 501 | **65,3** | 60 | **43,1** | 14,6 |

Rohvergleich davor → Ferien: **+2,0 pp** im Mittel, **+4,9 pp** bei ≥ 80 %. Der Anstieg fällt trotz gestiegenem Braun-Anteil an – bereinigt ist er also größer als 2 pp.

**Tabelle 3 – Balancierte Panels (gleiche Zeitreihen in beiden bzw. allen Perioden)**

| Panel | Serien | Ø davor % | Ø Ferien % | Δ pp | ≥ 80 % davor | ≥ 80 % Ferien | Δ pp |
|---|---:|---:|---:|---:|---:|---:|---:|
| A (davor + Ferien) | 1.012 | 58,5 | 59,8 | **+1,3** | 32,7 | 37,1 | +4,4 |
| B (alle drei) | 413 | 59,0 | 60,1 | **+1,1** | 33,6 | 38,0 | +4,4 |

Panel B nach Material (davor → Ferien → danach): Braun 36,5 → 31,2 → 43,7 · Grün 56,2 → 58,9 → 67,5 · Weiß 71,9 → 79,0 → 87,1. Nur Braun fällt in den Ferien; Grün und Weiß steigen.

**Tabelle 4 – Standortzentrierte Abweichung (Mittel der Zeitreihe = 0)**

| Periode | Ø Abweichung pp | sd pp | Anteil negativ % | Ø der Standortmittel % |
|---|---:|---:|---:|---:|
| davor | −1,80 | 21,9 | 49,7 | 55,3 |
| Ferien | **+0,50** | 18,9 | 45,3 | 59,1 |
| danach | +7,96 | 21,1 | 32,9 | 65,5 |

Nach Material (davor → Ferien): Braun +2,01 → −3,83 · Grün −2,24 → +1,45 · Weiß −3,50 → +2,89. Der Standort selbst liegt in den Ferien **2,3 pp über** seinem Juni/Juli-Wert; die Streuung ist mit rund 20 pp ein Vielfaches des Effekts.

**Tabelle 5 – Monatsdetail Juni–September 2026**

| Monat | n | Messtage | Ø gesamt % | Ø Braun | Ø Grün | Ø Weiß | ≥ 80 % ges. | overfull % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Juni | 1.501 | 21 | **53,7** | 32,9 | 50,5 | 64,2 | 24,7 | 5,2 |
| Juli | 1.310 | 22 | 61,4 | 36,7 | 63,6 | 81,2 | 39,2 | 5,0 |
| August | 1.215 | 21 | 57,5 | 32,4 | 58,5 | 77,4 | 33,5 | 2,8 |
| September | 858 | 16 | 64,1 | 37,3 | 64,5 | 82,2 | 42,7 | 10,6 |

Der Tiefpunkt liegt im **Juni**, nicht im Ferienfenster; die Ferien umfassen Juli-Hoch, August-Trog und September-Anstieg.

**Tabelle 6 – Kurzfenster und Basisrate**

| Prüfung | Ergebnis |
|---|---|
| 14 d vor Ferien (16.–29.07.) vs Ferien, Panel 483 Serien | 66,2 % → 57,3 % = **−8,9 pp**, ≥ 80 % 46,4 → 34,2 |
| Rollierende 14-Tage-Deltas, alle 334 Fenster | Median +0,4 pp, IQR −4,7 bis +5,0, Spanne −21,5 bis +27,0 |
| Delta zum Ferienstart 30.07. | **−4,7 pp** = 26. Perzentil aller Fenster |
| Delta 31.07. | −7,2 pp = 14. Perzentil |
| Größter Rückgang im Datensatz | −21,5 pp, Start 05.06.2026 (Pfingstferien-Ende) |

Gegen den Juligipfel sieht der Ferienstart wie ein Einbruch aus; gemessen an der normalen Fenster-zu-Fenster-Variation ist er ein **alltäglicher** Rückgang. Der Juni-Einbruch ist viermal so groß.

**Tabelle 7 – Zeitreihen-Klassifikation in den Ferien (nur Serien mit ≥ 2 Messungen, n = 440)**

| Kriterium | Braun | Grün | Weiß | Gesamt |
|---|---:|---:|---:|---:|
| Serien mit ≥ 2 Messungen | 106 | 164 | 170 | 440 |
| Ø < 50 % → Kandidat verlängertes Intervall | 88 | 49 | 7 | **144** (33 %) |
| davon nie ≥ 70 % erreicht (enge Kandidaten) | 86 | 49 | 7 | 142 |
| Ø ≥ 80 % → nicht drosseln | 2 | 36 | 99 | **137** (31 %) |
| mindestens eine Messung ≥ 80 % | 11 | 82 | 149 | 242 |
| nie ≥ 80 % | 95 | 82 | 21 | 198 |

`overfull` in den Ferien: 57 Messungen – Braun 1, Grün 14, **Weiß 42**. Über alle 1.099 in den Ferien gemessenen Serien (auch mit nur einer Messung) bleiben 262 Braun-, 126 Grün- und 32 Weiß-Serien im Mittel unter 50 %.

## Interpretation

- **Der Sommerrückgang ist der Juni, nicht die Ferien.** Juni 53,7 % ist der Jahrestiefstwert; er liegt acht Wochen vor Ferienbeginn. Vom 01.06. bis 29.07. steigen die Werte bereits wieder (Juli 61,4 %), die Ferien beginnen also auf einem Hoch.
- **Alle drei Abdeckungskontrollen zeigen keinen Ferienrückgang, sondern ein leichtes Plus.** Balanciertes Panel +1,3 pp (A) bzw. +1,1 pp (B), standortzentriert +2,3 pp, gleiches Gewicht je Standort +3,8 pp (55,3 → 59,1). Der Rohvergleich (+2,0 pp) ist damit nicht durch die Messauswahl verzerrt, sondern eher unterschätzt.
- **Der scheinbare Einbruch entsteht durch die Wahl des Referenzfensters.** Gegen die 14 Tage direkt vor Ferienbeginn fallen die Werte um 8,9 pp – aber genau dieses Fenster enthält das Julimaximum (Weiß 81,2 %, Median 90 %). Der Rückgang zum 30.07. liegt mit −4,7 pp auf dem 26. Perzentil aller 334 Vierzehn-Tage-Fenster, ist also ein gewöhnlicher Schwankungsschritt, kein Ferieneffekt.
- **Der Effekt ist materialspezifisch und gegenläufig.** Braun sinkt (35,3 → 32,3 %, standortzentriert −5,8 pp), Grün und Weiß steigen (Weiß +7,6 pp). Ein einziger Routen- oder Intervallschritt für „die Ferien“ würde die weiße Fraktion treffen, die ohnehin am vollsten ist: 42 `overfull`-Messungen in den Ferien, 99 von 170 Serien im Mittel ≥ 80 %.
- **Operativ heißt das: keine pauschale Drosselung, aber eine begründete Teilmenge.** 142 Zeitreihen bleiben in den Ferien durchgehend unter 70 % – zu 61 % Braun (86 von 142). Für diese ist ein um eine Stufe verlängertes Intervall plausibel. Alles andere (298 Serien) bleibt im Normalbetrieb, davon 137 mit einem Mittel ≥ 80 %, die bei Drosselung sofort Überlaufrisiko tragen.
- **Vorsichtige Empfehlung:** Intervallverlängerung nur für die 142 engen Kandidaten, nur während 30.07.–12.09., mit einer Obergrenze von einer Stufe und Rückfall auf Normalintervall, sobald eine Messung ≥ 80 % zeigt. Braun ist der einzige Materialstrang, für den das mengenmäßig trägt; Weiß bleibt vollständig außen vor. Wegen der dünnen Messdecke (1,5 Messungen je Serie in 45 Tagen) ist das eine Hypothese für einen Pilot, keine belegte Einsparung.

## Grenzen

- **Kein Leerungsdatum.** Füllstand ist Zeit seit letzter Leerung × Zulauf. Urlaubsabwesenheit, Hitze, Leerungsturnus und Meldeverhalten sind ohne Leerungsereignisse nicht trennbar; alle Aussagen sind deskriptiv, nicht kausal.
- **Genau eine Sommerpause im Datensatz** (ein Jahr, 2025-10 bis 2026-09). Keine Wiederholung, kein Vorjahresvergleich; Signifikanzaussagen wären bei n = 1 Saison nicht belastbar und werden nicht berichtet.
- **Ergebnis hängt an der Fensterwahl.** 90-Tage-Vergleich: +2,0 pp; Panel 59 Tage: +1,3 pp; Panel 14 Tage: −8,9 pp. Beide Richtungen sind im Datensatz, die Basisrate spricht gegen einen Ferieneffekt – das ist ein Argument, kein Beweis.
- **Ferientermine sind gesetzt, nicht gemessen.** 30.07.–12.09. als stadtweites Fenster; tatsächliche Abwesenheit einzelner Haushalte, Schulbezirke oder Gewerbekunden ist unbekannt.
- **Abdeckung ungleich:** 428 vs. 389 Standorte, 45,5 vs. 37,7 Messungen je Kalendertag, 2,2 vs. 1,5 je Serie. Das „danach“-Fenster (9 Messtage, 27,8 Messungen je Tag) ist nur als Trendhinweis lesbar.
- **Dünn gemessene Tage liegen systematisch höher** (in Analyse 12: Rangkorrelation Tages-n zu Tagesmittel −0,33). Die Ferien sind dünner besetzt – der leichte Anstieg könnte teilweise dieser Bias sein, nicht reale Füllhöhe.
- **Keine Behältergröße, kein Volumen, kein Gewicht.** Standortmittel behandeln alle Standorte gleich; ein 1,1-m³- und ein 10-m³-Behälter zählen identisch, Einsparungen in Fahrten sind daraus nicht ableitbar.
- `overfull` ist als 110 % kodiert, die tatsächliche Höhe unbekannt; die 10-pp-Rasterung begrenzt die Auflösung; `Location_id` bezeichnet einen Standort, nicht zwingend einen einzelnen Behälter.

## Nächster Schritt

Die 142 Kandidaten-Zeitreihen als Liste (Standort, Material, Ferien-Ø, Ferien-Maximum) exportieren und mit den tatsächlichen Leerungsterminen der Sommerferien 2026 abgleichen – erst damit ist prüfbar, ob dort bereits ein verlängertes Intervall gefahren wurde und ob es ohne Überlauf hielt.
