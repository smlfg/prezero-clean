# 25 – Standortdaten anreichern

> Die CSV enthält nur eine anonyme `Location_id` und (in einer separaten Datei)
> synthetische Koordinaten. Für echte Analyse fehlen Adresse, Stadtteil,
> Bebauung, Einzugsgebiet, Infrastruktur — alles, was erklärt, *warum* ein
> Standort voller ist.

## Frage

Welche Standortdaten würden die Analyse verbessern, und was lässt sich mit den
vorhandenen Daten schon anfangen?

## Vorgehen

Inventur der vorhandenen Standortinformationen, Bewertung der Anreicherungs-
quellen (Open Data Heilbronn, OSM, PreZero-Stammdaten) und einer
Machbarkeitsabschätzung, was sich mit synthetischen Koordinaten (nur Demo!)
schon rechnen lässt.

## Ergebnisse

### Was die CSV liefert

| Feld | Inhalt | Qualität |
|---|---|---|
| `Location_id` | 449 anonyme UUIDs | stabil, aber nicht rückführbar |
| `material_type` | brown/green/white | vollständig |
| `date`, `fill_level_perc` | Messung | kategorial, unregelmäßig |
| Koordinaten | `locations_synthetic.csv`, 449 Zeilen | **synthetisch**, Heilbronn-Bounding-Box |

Die synthetischen Koordinaten decken 49,06–49,24° N / 9,15–9,27° E ab — das
entspricht ungefähr Heilbronn, aber die Punkte sind gleichmäßig gestreut
(medianer Nächster-Nachbar-Abstand 0,18 km) und haben **keine** Korrelation
mit dem Füllstand (r(lat, mittlerer Füllstand) = −0,05, r(lon) = +0,05).
Sie sind für Demos nutzbar, für Analysen wertlos.

### Was fehlt — und was es ermöglichen würde

| Fehlende Dimension | Mögliche Quelle | Analyse, die sie ermöglicht |
|---|---|---|
| Echte Adresse/Koordinaten | PreZero-Stammdaten | Routenoptimierung (24), Pilotgebiete (32) |
| Stadtteil/Bezirk | Heilbronn Open Data | Standortvergleich (08), Cluster (09) |
| Wohn-/Gewerbegebiet | OSM landuse, Zensus | Lokale Einflussfaktoren (26), Kapazität (27) |
| Haushaltsdichte/Einwohner | Zensus 2022 | Nachfrageprognose (21), Saisonalität (11) |
| Gastronomie/Geschäfte/Schulen | OSM POI | Standortvergleich, Cluster |
| Entfernung zum Betriebshof | PreZero | Routenplanung (24), Kosten (30) |
| Containerkapazität/-größe | PreZero-Stammdaten | Kapazitätsplanung (27), Größenbewertung (28) |
| Leerungszeiten (historisch) | PreZero | Leerungen identifizieren (16), Zyklen (17) |
| Wetter/Veranstaltungen | DWD, Eventkalender | Lokale Einflussfaktoren (26), Anomalien (15) |

### Was mit den vorhandenen Daten schon geht

- Standort als **stabile Dimension** für Rankings, Cluster und Zeitreihen —
  auch ohne Geodaten.
- Relative Lage: welche Standorte sind im Vergleich zueinander auffällig
  (Top/Bottom, Cluster) — das braucht keine Koordinaten.
- Materialeffekte innerhalb eines Standorts (Analyse 10) — Standort als
  Kontrollvariable.
- Saisonale Muster (Analyse 11) — standortunabhängig.

### Was erst mit Anreicherung möglich wird

- Erklärung *warum* ein Standort voller ist (Wohngebiet vs. Gewerbe).
- Echte Routenoptimierung und Fahrtkosten.
- Kausale Tests (z. B. „Gastronomie-Dichte → höhere Weiße-Glas-Auslastung").
- Digitaler Zwilling (35) mit räumlicher Auflösung.

## Grenzen

Ohne echte Koordinaten bleibt jede räumliche Aussage spekulativ. Die
synthetischen Koordinaten dürfen nicht für Analysen verwendet werden, die
echte Entfernungen oder Nachbarschaften behaupten. Die Anreicherung selbst
ist ein Datenbeschaffungsprojekt, keine Analyse — sie braucht Vereinbarungen
mit PreZero (Stammdaten) und Open-Data-Quellen.

## Nächster Schritt

Eine Anreicherungs-Checkliste (Felder + Quelle + Aufwand) mit dem Mentor
abstimmen; im Prototypen ein `site`-Objekt mit leeren Feldern für Adresse/
Koordinaten/Stadtteil vorsehen, damit die CSV-Dimension `Location_id` später
nahtlos ersetzt werden kann.