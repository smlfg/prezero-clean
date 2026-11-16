# 24 – Routenplanung vorbereiten

> Die CSV liefert eine gewichtete, priorisierte Stoppliste mit Standort-ID,
> Dringlichkeit und Materialien — genug als Eingabe für einen Routenoptimierer.
> Echte Koordinaten, Leerungsdauer, Fahrzeugkapazität und Zeitfenster fehlen
> vollständig; die synthetischen Koordinaten dürfen nur als Demo dienen.

## Frage

Was liefert die CSV bereits für eine Tour, und was fehlt?

## Vorgehen

(a) Stoppliste aus Stichtag 2026-03-15 (nur Daten davor) mit Feldern
stop_id, priority, weight, materials, lat, lon, service_time_min. (b) Liste der
fehlenden Tourdaten mit Auswirkung. (c) Machbarkeitscheck mit synthetischen
Koordinaten (Haversine, Nearest-Neighbour vs. Zufall). (d) Fragen an den Mentor.

## Ergebnisse

### (a) Stoppliste — Schema und Beispiel

Eingabe für einen Routenoptimierer (VRP) aus der CSV ableitbar:

| Feld | Quelle in CSV / Berechnung |
|---|---|
| stop_id | `Location_id` |
| priority | prognostizierter Füllstand (0–110) + Bonus kritische Materialien |
| weight | Anzahl kritischer Materialien (0–3) |
| materials | Liste der Materialien am Standort |
| lat, lon | `locations_synthetic.csv` (synthetisch!) |
| service_time_min | **nicht in CSV** — Annahme nötig |
| time_window | **nicht in CSV** |

Am Stichtag 2026-03-15: 421 Standorte, davon 404 mit mindestens einem
kritischen Material, 137 mit allen drei. Top-30-Stopps haben priority = 110
(alle drei Materialien overfull).

### (b) Was die CSV NICHT liefert

| Fehlende Größe | Auswirkung auf die Route |
|---|---|
| Echte Koordinaten/Adressen | Keine echte Fahrstrecke; synthetische Koordinaten sind Platzhalter |
| Leerungsdauer pro Stopp | Servicezeit muss geschätzt werden (z. B. 5–15 min) |
| Fahrzeugkapazität (Volumen/Gewicht) | Keine Kapazitätsbeschränkung modellierbar |
| Zeitfenster (Öffnungszeiten, Lärm) | Keine realistischen Tourenzeiten |
| Verkehrs-/Straßennetz | Luftlinie unterschätzt echte Fahrstrecke (Faktor 1,3–1,6) |
| Leerungsereignisse (historisch) | Keine Kalibrierung der Servicezeit |
| Fahrzeuganzahl/Kapazität des Fuhrparks | Keine Multi-Vehicle-Routing |

### (c) Machbarkeitscheck (synthetische Koordinaten, Heilbronn-Bounding-Box)

Top-30-Stopps, Haversine-Distanzmatrix:

| Strategie | Gesamtstrecke |
|---|---:|
| Nearest-Neighbour-Tour | 49,1 km |
| Zufallsreihenfolge (Mittel aus 200) | 106,6 km |
| Zufallsreihenfolge (Minimum) | 85,7 km |

Nearest-Neighbour halbiert die Strecke gegenüber Zufall — zeigt, dass die
Prioritätsliste sich in eine Tour überführen lässt. **Aber:** die Koordinaten
sind synthetisch (alle im 49,06–49,24° N / 9,15–9,27° E Rechteck, medianer
Nächster-Nachbar-Abstand 0,18 km), also keine echte Fahrstrecke.

### (d) Fragen an den PreZero-Mentor

1. Gibt es echte Standortstammdaten (Adresse, Koordinaten, Stadtteil) für die
   449 `Location_id` — und darf der Prototyp sie nutzen?
2. Welche Leerungszeiten (min/Stopp), Fahrzeugtypen und Kapazitäten nutzt
   PreZero, und gibt es Zeitfenster (Wohngebiete, Schulen, Gewerbe)?
3. Gibt es historische Touren-/GPS-Daten, um Servicezeiten und echte
   Fahrdistanzen zu kalibrieren?

## Grenzen

Die gesamte Routenanalyse ist eine Demo mit Platzhalterkoordinaten. Echte
Tourenoptimierung ist ohne die Daten aus (b) und (d) nicht möglich — jede
Fahrstrecke, die aus dieser CSV abgeleitet wird, wäre eine Fiktion.

## Nächster Schritt

Die drei Mentor-Fragen als Block in das Pitch-Dokument aufnehmen und die
Stoppliste als stabiles JSON-Schema (`stop_id, priority, weight, materials,
lat, lon, service_time_min`) definieren, damit der echte Optimierer später
nur Daten austauschen muss, nicht die Schnittstelle.