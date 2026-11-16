# 35 – Grundlage für einen digitalen Zwilling schaffen

> Die CSV liefert eine erste Datenbasis: Standort × Material × Zeit × Füllstand.
> Für einen digitalen Zwilling fehlen aber Kapazität, Leerungsereignisse,
> echte Geodaten und Sensormetadaten — also vier der fünf Kerndimensionen.

## Frage

Was kann die CSV heute schon als Grundlage für einen digitalen Zwilling leisten,
und was fehlt?

## Vorgehen

Inventur der vorhandenen Dimensionen, Abbildung auf ein Zwilling-Datenmodell,
Bewertung der Reife (was ist beobachtet vs. abgeleitet vs. unbekannt) und
eine Roadmap für den Ausbau.

## Ergebnisse

### Vorhandene Dimensionen

| Dimension | In CSV? | Qualität |
|---|---|---|
| Standort (Location_id) | ja (449) | anonym, stabil |
| Material (brown/green/white) | ja | vollständig |
| Zeit (Datum) | ja (229 Messtage) | unregelmäßig, keine Zeitstempel |
| Füllstand | ja (kategorial) | 10%-Schritte + overfull |
| Kapazität (Volumen) | nein | unbekannt |
| Leerungsereignisse | nein | nur indirekt (Analyse 16) |
| Echte Geodaten | nein (synthetisch) | Platzhalter |
| Sensormetadaten | nein | unbekannt (Typ, Kalibrierung) |
| Fahrzeug-/Tourdaten | nein | unbekannt |

### Zwilling-Datenmodell (Vorschlag)

```
Site (Location_id)
 ├── Container (material_type, capacity_l, sensor_id)
 │    └── Reading (date, fill_level, quality_flag)
 ├── Location (address, lat, lon, district, poi)
 └── CollectionEvent (date, volume_collected, vehicle_id, duration_min)
```

Die CSV füllt heute: `Site.id`, `Container.material`, `Reading.date`,
`Reading.fill_level`. Die anderen Felder sind leer.

### Reifegrad der Analyse-Ergebnisse

| Ergebnis | Reife | Basis |
|---|---|---|
| Füllstandshistorie je Standort/Material | beobachtet | CSV |
| Materialeffekte | beobachtet | CSV |
| Saisonale Muster | beobachtet | CSV (1 Jahr) |
| Leerungszyklen | abgeleitet | negative Sprünge (unsicher) |
| Prognosen | abgeleitet | MAE 20–27 pp |
| Standortcluster | abgeleitet | Silhouette 0,19 (schwach) |
| Routen | nicht möglich | keine Koordinaten |
| Kapazitätsplanung | nicht möglich | keine Volumina |

### Roadmap für den Ausbau

1. **Phase 1 (jetzt):** CSV als statische Datenbasis, Analysen 01–36 als
   Dokumentation des Systemverhaltens.
2. **Phase 2 (mit PreZero-Stammdaten):** echte Koordinaten, Kapazitäten,
   Leerungsereignisse nachladen — dann werden Routen, Kapazitätsplanung und
   Kausalanalysen möglich.
3. **Phase 3 (mit Sensordaten):** Echtzeit-Füllstände, tägliche Prognosen,
   Live-Dashboard, automatische Tourenvorschläge.
4. **Phase 4 (mit externen Daten):** Wetter, Events, Bevölkerung — Erklärung
   lokaler Unterschiede.

### Was der Zwilling heute leisten kann

- Historische Analyse und Reporting (Monats-/Quartalsberichte).
- Priorisierungshilfe für die Disposition (Warnliste, Score).
- Hypothesengenerierung (welche Daten fehlen? → Analyse 36).
- Demo und Pitch (Visualisierung des Containerverhaltens).

### Was er heute NICHT leisten kann

- Echtzeit-Monitoring.
- Automatische Tourenplanung.
- Kapazitätsplanung mit Volumina.
- Kausale Erklärungen.

## Grenzen

Der Begriff „digitaler Zwilling" ist hier bewusst bescheiden verwendet: eine
statische Datenbasis mit abgeleiteten Kennzahlen, kein Live-Modell. Erst mit
Echtzeit-Sensordaten und Leerungsereignissen wird daraus ein echter Zwilling.
Die CSV ist eine erste, wertvolle, aber unvollständige Grundlage.

## Nächster Schritt

Datenmodell (Site/Container/Reading/CollectionEvent) als Schema dokumentieren
und die CSV-Importpipeline so bauen, dass PreZero-Stammdaten (Phase 2) ohne
Strukturänderung nachgeladen werden können.