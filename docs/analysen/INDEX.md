# Index der Analysen (36 Datenanalysen, 14.11.2026)

Diese 36 Analysen sind die Datengrundlage der Pitch-Aussagen. Einzelne Analysen können überholt sein, wenn ein späteres Modell sie ersetzt hat (siehe Spalte Profil und `docs/archiv/`).

**Dokumentenübersicht:** [../INDEX.md](../INDEX.md) · **Status:** [../STATUS.md](../STATUS.md)

## 1. Risiko & Priorisierung (01–05)

| Nr | Titel | Kernaussage | Wichtigste Kennzahl | Profil |
|---:|---|---|---|---|
| 01 | [Überfüllungsrisiken erkennen](01_ueberfuellungsrisiko.md) | Das Überfüllungsrisiko konzentriert sich auf Weißglas und die Monate Januar bis Mai. | 44,7 % ≥80 %; 10,2 % overfull | Modell |
| 02 | [Container priorisieren](02_priorisierung.md) | Ein transparenter Score priorisiert 19 Serien über 90 Punkte. | 19 Serien >90 Punkte | Modell |
| 03 | [Leerungsintervalle optimieren](03_leerungsintervalle.md) | Aus beobachteten Steigraten lassen sich kürzere und längere Intervalle ableiten. | 399 kürzere, 546 längere Intervalle | Modell |
| 04 | [Füllgeschwindigkeit](04_fuellgeschwindigkeit.md) | Die scheinbare Füllrate sinkt stark mit dem Messabstand. | Median 0,74 pp/Tag | Daten |
| 05 | [Zeit bis zum erwarteten Überlauf](05_zeit_bis_ueberlauf.md) | Ein Teil der Reihen ist bereits kritisch oder erreicht 80 % kurzfristig. | 462 von 1.338 Reihen ≥80 % | Modell |

## 2. Material & Standort (06–10)

| Nr | Titel | Kernaussage | Wichtigste Kennzahl | Profil |
|---:|---|---|---|---|
| 06 | [Materialvergleich](06_materialvergleich.md) | Die Rangfolge der Auslastung ist standortübergreifend Braun < Grün < Weiß. | Weiß liegt an 429 von 441 Standorten über Braun | Daten |
| 07 | [Materialabhängige Schwellenwerte](07_material_schwellenwerte.md) | Schwellenwerte sollten materialabhängig gesetzt werden. | Weiß 80 %, Grün 70 %, Braun 60 % | Modell |
| 08 | [Standortvergleich](08_standortvergleich.md) | Material erklärt mehr Varianz als der Standort, dessen Rangfolge zudem instabil ist. | Material 28,7 %, Standort 8,6 % | Daten |
| 09 | [Standorte clustern](09_standort_cluster.md) | Die vier Cluster trennen nur schwach; das Verhalten liegt überwiegend auf einem Kontinuum. | Silhouette 0,19 | Modell |
| 10 | [Standortkopplung](10_standort_kopplung.md) | Die drei Materialien eines Standorts bewegen sich an gemeinsamen Messtagen häufig gemeinsam. | Median r = 0,66 | Daten |

## 3. Saison & Zeit (11–18)

| Nr | Titel | Kernaussage | Wichtigste Kennzahl | Profil |
|---:|---|---|---|---|
| 11 | [Saisonale Nachfrage](11_saisonalitaet.md) | Zwischen Juni und März liegt ein deutlicher, nicht durch Standortzusammensetzung erklärter Saisonabstand. | 53,7 % bis 85,2 %; 31,5 pp | Daten |
| 12 | [Ferien- und Feiertagseffekte](12_ferien_feiertage.md) | Ein eigenständiger Ferieneffekt ist von Saison und Abdeckung nicht trennbar. | Abweichungen meist höchstens 7 pp | Daten |
| 13 | [Nachweihnachts-Spitzen](13_nachweihnachtsspitze.md) | Die auffälligste Spitze liegt in der ersten Messrunde nach dem Jahreswechsel. | 59 von 112 overfull (52,7 %) | Daten |
| 14 | [Sommer- und Urlaubsperioden](14_sommer_urlaub.md) | Eine pauschale Intervallverlängerung für die Sommerferien ist nicht belegt. | Nur 144 von 440 Reihen differenziert | Daten |
| 15 | [Anomalien erkennen](15_anomalien.md) | Große Sprünge sind überwiegend Folge langer Beobachtungslücken. | 13,1 % der Übergänge | Modell |
| 16 | Mögliche Leerungen identifizieren *(archiviert seit `127d502`)* | Negative Sprünge als Leerungsbehelf — ersetzt durch das Timer-Modell. | 936 von 10.363 Übergängen | Modell |
| 17 | [Leerungszyklen rekonstruieren](17_leerungszyklen.md) | Vollständige Zyklen sind erkennbar, aber nur wenige Reihen sind regelmäßig. | Median 46 Tage; 17,9 % regelmäßig | Modell |
| 18 | [Unregelmäßige Messungen erkennen](18_messluecken.md) | Ein Drittel der Reihen enthält Lücken über 90 Tage und ist für Prognosen eingeschränkt. | 458 Reihen mit >90-Tage-Lücke | Daten |

## 4. Qualität & Prognose (19–22)

| Nr | Titel | Kernaussage | Wichtigste Kennzahl | Profil |
|---:|---|---|---|---|
| 19 | [Datenqualität bewerten](19_datenqualitaet.md) | Die CSV ist strukturell sauber, aber inhaltlich dünn und kategorial. | 10,2 % overfull ohne Höhenangabe | Daten |
| 20 | [Messabdeckung bewerten](20_messabdeckung.md) | Häufiger gemessene Standorte haben im Mittel höhere Füllstände. | Median 24 Messungen/Standort; r = 0,39 | Daten |
| 21 | [Prognosemodell für Füllstände](21_prognosemodell.md) | Der Material-Median ist die beste getestete einfache Baseline. | MAE 21,0 pp; 66,3 % innerhalb ±20 pp | Modell |
| 22 | [Überlaufwahrscheinlichkeit prognostizieren](22_ueberlaufwahrscheinlichkeit.md) | Ein materialabhängiges Bucket-Modell verbessert die Basisrate. | Brier 0,196 statt 0,249 | Modell |

## 5. Betrieb & Strategie (23–36)

| Nr | Titel | Kernaussage | Wichtigste Kennzahl | Profil |
|---:|---|---|---|---|
| 23 | [Dynamische Leerungsempfehlungen](23_dynamische_empfehlungen.md) | Eine tagesaktuelle Liste ist möglich, bleibt aber saisonal volatil. | Top-20-Überlappung März/Juli: 10–25 % | Konzept |
| 24 | [Routenplanung vorbereiten](24_routenplanung_vorbereitung.md) | Die CSV liefert eine priorisierte Stoppliste, aber keine produktionsfähige Route. | 4 zentrale Routendaten fehlen | Konzept |
| 25 | [Standortdaten anreichern](25_standort_anreicherung.md) | Für die Erklärung von Standortunterschieden fehlen Stammdaten und Kontext. | Anonyme Location_id statt Adresse | Konzept |
| 26 | [Lokale Einflussfaktoren untersuchen](26_lokale_einflussfaktoren.md) | Gemeinsames Verhalten ist nur ein Indiz für lokale Treiber. | Median r = 0,66 | Konzept |
| 27 | [Kapazitätsplanung unterstützen](27_kapazitaetsplanung.md) | Zusätzliche Kapazität ist vor allem bei Weißglas dringlich. | 61,3 % aller overfull-Messungen | Modell |
| 28 | [Containergößen oder Aufstellorte bewerten](28_containergroessen_aufstellorte.md) | Die große Weiß-Braun-Differenz spricht für materialabhängige Behältergrößen. | 359 von 441 Standorten >30 pp Differenz | Daten |
| 29 | [Servicequalität messen](29_servicequalitaet.md) | Die beobachtete Servicequalität schwankt stark über das Jahr. | März 37,6 % vs. Juni 5,2 % overfull | Konzept |
| 30 | [Kosten und Ressourcen planen](30_kosten_ressourcen.md) | Eine bedarfsgesteuerte Planung kann die kritischen Anfahrten fokussieren. | Median 13, Spitze 40 Standorte/Tag | Konzept |
| 31 | [Einsparpotenziale finden](31_einsparpotenziale.md) | Einsparungen liegen eher in Bündelung und saisonaler Drosselung als in dauerhaft leeren Standorten. | 9 von 449 nie kritisch | Konzept |
| 32 | [Pilotgebiete vergleichen](32_pilotgebiete.md) | Vier Gruppen sind unterscheidbar, aber nicht scharf getrennt. | 119/107/105/118 Standorte | Modell |
| 33 | [Geschäftliche Kennzahlen erzeugen](33_geschaeftliche_kennzahlen.md) | Ein kompaktes KPI-Set kann direkt aus der CSV gebildet werden. | Mittelwert 66,0 %; 10,2 % overfull | Konzept |
| 34 | [Dashboard für Disposition bauen](34_dashboard.md) | Die CSV trägt Ranglisten, Zeitreihen, Materialvergleiche und Warnlisten. | 5 Dashboard-Bausteine | Konzept |
| 35 | [Grundlage für einen digitalen Zwilling](35_digitaler_zwilling.md) | Die CSV bildet Standort, Material, Zeit und Füllstand ab, aber nicht den Betriebskontext. | 4 von 5 Kerndimensionen fehlen | Konzept |
| 36 | [Hypothesen für den Mentor](36_hypothesen_mentor.md) | Die CSV zeigt das Verhalten, nicht dessen Ursachen. | 5 zentrale Datenlücken | Konzept |

## Empfohlene Lesereihenfolge für den Pitch

1. [01 – Überfüllungsrisiken erkennen](01_ueberfuellungsrisiko.md)
2. [06 – Materialvergleich](06_materialvergleich.md)
3. [11 – Saisonale Nachfrage](11_saisonalitaet.md)
4. [22 – Überlaufwahrscheinlichkeit prognostizieren](22_ueberlaufwahrscheinlichkeit.md)
5. [23 – Dynamische Leerungsempfehlungen](23_dynamische_empfehlungen.md)

## Inkonsistenzen

- **Monatsmittel:** Die Gesamtanalyse weist für März 84,6 % und Juni 52,4 % aus. Analyse 11 nennt 85,2 % bzw. 53,7 %, Analyse 14 nennt für Juni ebenfalls 53,7 %. Die Abweichungen betragen 0,6 bzw. 1,3 Prozentpunkte; die zugrunde liegende Teilmenge oder Filterung ist in der Gesamtanalyse nicht ausgewiesen.
- **Keine weiteren festgestellten Abweichungen** bei den gemeinsam ausgewiesenen Gesamtwerten: 11.701 Messungen, 449 Standorte, 1.338 Reihen, Materialmittel, Anteile ≥80 %, overfull-Anteil sowie die KPIs in Analyse 33 stimmen mit der Gesamtanalyse überein.
