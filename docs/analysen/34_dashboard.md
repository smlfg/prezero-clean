# 34 – Dashboard für Disposition bauen

> Die CSV trägt fünf Dashboard-Bausteine: Karten (sobald echte Koordinaten
> vorliegen), Ranglisten, Zeitreihen, Materialvergleiche und Warnlisten.
> Ohne echte Koordinaten ist die Karte nur mit synthetischen Platzhaltern
> möglich.

## Frage

Wie lässt sich ein Dispositions-Dashboard aus den Daten aufbauen?

## Vorgehen

Inventur der verfügbaren Dashboard-Komponenten, Datenanforderungen pro
Komponente, Vorschlag einer Informationsarchitektur (Startseite → Detail) und
einer Priorisierung für den Hackathon (was ist in 2 Tagen machbar).

## Ergebnisse

### Fünf Bausteine

| Baustein | Datenquelle | Machbar in 2 Tagen? |
|---|---|---|
| Warnliste (Top kritische Standorte) | CSV + Scoring (02) | ja |
| Rangliste (Priorität, Material, Standort) | CSV + Scoring (02) | ja |
| Zeitreihen (Füllverlauf je Standort/Material) | CSV | ja |
| Materialvergleich (Braun/Grün/Weiß) | CSV | ja |
| Karte (Standorte farbcodiert) | synthetische Koordinaten (Demo) | ja, mit Platzhaltern |
| Saisonale Ansicht (Monatsmittel) | CSV | ja |

### Vorgeschlagene Informationsarchitektur

1. **Startseite (Disposition):** Warnliste (Top 20 kritische Standorte heute),
   KPI-Kacheln (mittlerer Füllstand, Überfüllungsquote, kritische Stopps/Tag,
   Service-Score), Materialvergleich als Balkendiagramm.
2. **Standort-Detail:** Zeitreihe (Füllstand über Zeit), Messhistorie,
   Prognose (Tage bis 80/100 %), Materialien am Standort, Cluster-Zuordnung.
3. **Analyse-Ansicht:** Saisonale Muster, Ferien-/Feiertagseffekte, Cluster,
   Anomalien — für den Disponenten als Kontext, nicht als Pflicht.
4. **Datenqualität:** Messabdeckung, Lücken, Anomalien — für Transparenz.

### Komponenten und ihre Datenanforderungen

| Komponente | Pflichtfelder | Optionale Felder |
|---|---|---|
| Warnliste | Location_id, Material, letzter Wert, Datum, Score | Prognose, Cluster |
| Rangliste | Location_id, Score, Material, Mittelwert, Rate | Segment |
| Zeitreihe | Location_id, Material, Datum, Wert | Prognoseband |
| Karte | Location_id, lat, lon, Farbe (Score) | Cluster, Material |
| Materialvergleich | Material, Mittelwert, ≥80 %, overfull | Boxplot je Standort |
| Saisonal | Monat, Material, Mittelwert | Standort-Filter |

### Priorisierung für den Hackathon (2 Tage)

1. Warnliste + KPI-Kacheln (Tag 1, Vormittag) — höchster operativer Wert.
2. Zeitreihe je Standort (Tag 1, Nachmittag) — erklärbar, überzeugend im Pitch.
3. Materialvergleich + Saisonal (Tag 2, Vormittag) — Kontext.
4. Karte mit synthetischen Koordinaten (Tag 2, Nachmittag) — Demo-Effekt,
   aber klar als Platzhalter markieren.

### Technische Hinweise

- Datenquelle: CSV + berechnete Scores (Analyse 02/05/23). Kein Backend nötig
  für den Prototypen — statische JSON-Dateien reichen.
- Koordinaten: `locations_synthetic.csv` verwenden, aber im UI als
  „synthetische Platzhalter" kennzeichnen.
- Aktualisierung: batch (täglich neu berechnen), keine Echtzeit.

## Grenzen

Ohne echte Koordinaten ist die Karte eine Illustration. Ohne Echtzeit-Messungen
ist das Dashboard ein tägliches Reporting, kein Live-Monitoring. Die Warnliste
basiert auf prognostizierten Werten (MAE ≈ 20–27 pp) — sie ist eine
Priorisierungshilfe, keine Gewissheit.

## Nächster Schritt

Dashboard-Skizze (Wireframe) mit dem Team abstimmen und die vier priorisierten
Komponenten mit statischen Daten umsetzen; echte Koordinaten nachliefern, sobald
PreZero sie freigibt.