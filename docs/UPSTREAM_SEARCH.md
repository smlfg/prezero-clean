# UPSTREAM_SEARCH — Drehbuch (Szenario-Dateien) + Vorschau-Bilder LKW-Objekte

**Slice:** Drehbuch-Dateien für das Simulations-Kino · LKW-Objekt-Katalog mit Vorschau-Bildern
**Datum:** 2026-11-16
**Gate:** `03_HAI/docs/UPSTREAM_FIRST_GATE.md` (fail-closed, ≥3 Kandidaten)

## Need

Das Kino braucht (a) ein **Drehbuch**: vom Nutzer wählbare Szenarien als Datei, die
Abstand, LKW-Anzahl, Strategie und Schwelle in die Simulation einspeisen, plus ein
**LKW-Etikett** (Typ + Ladevolumen); und (b) für verschiedene LKW-Objekte
**Vorschau-Bilder** im Drehbuch.

> **Fassung 2:** Die LKW-Kapazität ist **nur ein Platzhalter** — sie speist **nichts** in die
> Simulation ein. Grund: die Daten zeigen *ein Besuch je Ort* und *keine beobachtete Ladung
> über 6,4 m³*; eine Kapazität im Modell würde entweder den Ist-Lauf zerstören oder nichts
> bewirken (Beleg unten). Deshalb **kein A7, kein Eingriff in `engine.js`/`sim_referenz.py`**,
> kein `SCOPE.md`-Konflikt. Der Upstream-Slice bleibt unverändert.

## Kandidaten

### A — Drehbuch / Szenario-Dateien (Konfiguration, Validierung, Presets)

| # | Kandidat | URL | Lizenz | Andock-Idee | Verdict |
|---|---|---|---|---|---|
| A1 | `jsonschema` (python-jsonschema) | https://github.com/python-jsonschema/jsonschema | MIT | JSON-Schema für das Drehbuch-Format; Validierung in `scripts/drehbuch_pruefen.py` und als pytest-Fixture | **use** |
| A2 | `check-jsonschema` (CLI + pre-commit) | https://github.com/python-jsonschema/check-jsonschema | MIT | CLI-Validierung der Drehbuch-Dateien im CI/pre-commit | **use** (als CLI, optional) |
| A3 | `pytest-jsonschema` (collective) | https://github.com/collective/pytest-jsonschema | MIT | Drehbuch-Dateien als pytest-Fälle validieren — Deckung mit A1, kein Vorteil | reject (redundant zu A1) |
| A4 | `inab/python-extended-json-schema-validator` | https://github.com/inab/python-extended-json-schema-validator | MIT | Erweiterte Schema-Validierung | reject (overkill für 6 Felder) |

**Decision A: `jsonschema` (A1) + `check-jsonschema` (A2).**
Begründung: Das Drehbuch braucht ein **prüfbares Schema**, sonst driftet Datei und
Dokument auseinander — genau das, was `AGENTS.md` §6 und der KINO-Vertrag §7 (Herkunftsmarkierung)
verhindern wollen. A1 ist ein reines Python-Modul ohne Build-Schritt und passt zur
`file://`-Doppelklick-Anforderung des Kinos. Kein Build, kein Bundler, kein npm.

### B — Vorschau-Bilder der LKW-Objekte

| # | Kandidat | URL | Lizenz | Andock-Idee | Verdict |
|---|---|---|---|---|---|
| B1 | **matplotlib** (Skizzen/Silhouetten selbst zeichnen) | https://matplotlib.org | BSD-3 | LKW-Seitenansicht als **schematische Silhouette** (Cabine + Aufbau) aus den Volumenangaben der Hersteller; PNG via `scripts/bilder.py`-Muster | **use** |
| B2 | Three.js + GLTF (Fahrzeug-3D-Viewer) | https://threejs.org | MIT | Interaktive 3D-LKW-Ansicht | **reject** — verletzt `SCOPE.md` („UI" nicht im Scope) und `assets/ui/UI_REGELN.md` §4 (kein JS, keine Interaktion, max. 3 Bilder); braucht GLB-Assets, Build-Step und Netz — bricht `file://` |
| B3 | `schemdraw` | https://schemdraw.readthedocs.io | MIT | Schematische technische Zeichnung | reject (Chemie-/Elektrotechnik-Fokus, kein Fahrzeugbezug) |
| B4 | `svg2mpl` / `skunk` | https://pypi.org/project/svg2mpl/ · https://github.com/whitead/skunk | MIT | SVG in matplotlib rendern | reject (bringt SVG-Assets mit, die dann doch von Hand wären) |
| B5 | Icon-Packs (Matita, Plotcaster, IconHub) | div. | MIT | fertige LKW-Icons | reject — generische Icons ohne Ladevolumen-Bezug; „Vorschau" würde Behauptung zeigen, nicht Beleg |

**Decision B: matplotlib (B1), schematische Seitenansicht.**
Begründung: `assets/ui/UI_REGELN.md` verbietet JS/Interaktion und erlaubt **statische PNGs**
(1600×900) mit direkter Beschriftung. Die Vorschau muss **eine Aussage** stützen: *wie viel passt
auf dieses LKW, im Vergleich zu einem vollen PreZero-Standort (6,4 m³)*. Das ist eine
Maß-Angabe, keine Ästhetik. Ein 3D-Viewer (B2) wäre Technik für die Technik.

### C — LKW-Objekt- und Volumenangaben (Datenquelle, nicht Code)

| # | Quelle | URL | Verwendet für |
|---|---|---|---|
| C1 | Stummer Glass Collector GC 23 (Fact Sheet PDF) | https://stummer.net/wp-content/uploads/2026/03/260330_STU_Fact_Sheet_Glassammpler_A4_ENGL.pdf | Glas-Sammelfahrzeug: **23 m³ max. Ladevolumen**, 26 t, 2-Kammer |
| C2 | Zoeller MEDIUM X4/X4H | https://www.zoeller-kipper.de/wp-content/uploads/2024/02/2022.06.07_MEDIUM-X4H.pdf | Hecklader: **14–29 m³** Nutzvolumen, Ladeförderer 6,2 m³/min |
| C3 | Zoeller/Stummer Eurolift Hooklift | https://stummer.net/en/products/ | Hakenlift: **18–31 m³** |
| C4 | REMONDIS Recycling Schweiz (Fuhrpark) | https://www.remondis-recycling.ch/ueber-uns/behaelter-und-fahrzeuge/ | Fahrzeugtypen: Hakenlift, Überkopflader, Absetzkipper |
| C5 | REMONDIS Sammelsysteme (PDF) | https://machulez-logistik.de/wp-content/uploads/2022/07/Remondis-Sammelsysteme-fuer-die-Kreislaufwirtschaft.pdf | ASKM 7/10 m³, ARKM 11–48,5 m³, U 2,5/5,0 m³ |

**Decision C: C1–C5 als Quelle für `docs/externe_parameter.md` V-5 „LKW-Objekte".**
Diese Werte sind **recherchiert**, nicht gemessen, nicht erfunden. Sie landen ausschließlich
in der Vorschau und in der A7-Referenz.

## Beleg: die Zahlen, die das Drehbuch tragen

Aus `data/raw/glass_fill_levels_anonymized_f.csv` (4.468 Besuche, A6/V-3):

| Größe | Wert | Art |
|---|---|---|
| Ladung je Besuch, untere Schranke (nur gemessene Kammern) | Median **3,61 m³** · P90 5,63 · max 6,40 | gemessen + A6 |
| Ladung je Besuch, obere Schranke (alle Farben, `overfull` = voll) | Median **4,35 m³** · P90 5,86 · max 6,40 | gemessen + A6 |
| Anteil Besuche mit Ladung > 6,4 m³ | **0,0 %** | gemessen + A6 |
| Volumen eines 3-Kammer-Standorts bei 100 % | **6,4 m³** (3,2 + 2,1 + 1,1) | A6/V-3, modelliert |
| Zufluss vs. Entnahme je Kammer | Anteil Zufluss > Entnahme **47,4 %** | gemessen + A6 |

**Folgerung (der Kern von A7):** Der beobachtete Rhythmus ist bilanziert, und **kein
beobachteter Besuch** überschreitet 6,4 m³. Ein LKW mit ≥ 6,4 m³ nimmt also **jede** beobachtete
Ladung vollständig mit. Jede kleinere Kapazität lässt Glas stehen → das System flutet
(Überlauf 4,91 % → ~96 %, nachgerechnet). Größere Kapazität ist im Modell **nicht
unterscheidbar**, weil kein Mehrfach-Stopp pro Tour belegt ist (Daten: ein Besuch = ein Ort).

## Status

**PARKED für den Code-Teil** — der Upstream-Slice (A1+A2+B1) ist identifiziert und
verdrahtungsfähig, aber die Umsetzung wartet auf die Freigabe von Samuel zur
Scope-Erweiterung (LKW-Kapazität steht in `SCOPE.md` unter „Nicht im Scope").
Kein Feature-Code geschrieben.

## Offene Punkte für Samuel

1. `SCOPE.md` verbietet „LKW-Kapazität" ausdrücklich. Vorschlag: Ausnahme-Notiz aufnehmen.
2. `AGENTS.md` §5 hat Volumen-Steuerung **parkiert** (V-4 „Parkierte Optionen"). Das Drehbuch
   ist **keine Optimierung**, sondern Szenario-Darstellung — die Zielzahl (§5) bleibt
   „eingesparte Leerungen in %". Bitte bestätigen, dass Parkierung die Optimierung meint,
   nicht die Darstellung.
3. LOC-Budget für den Glue (A1/A2/B1): ~80 Zeilen Default-Budget, darüber nur mit neuer Freigabe.

---

## Anhang — Fassung 2: Warum die Kapazität ein Platzhalter bleibt

### Der Befund (aus `data/raw/glass_fill_levels_anonymized_f.csv`, 4.468 Besuche, + A6/V-3)

| Größe | Wert | Art |
|---|---|---|
| Ladung je Besuch, untere Schranke (nur gemessene Kammern) | Median **3,61 m³** · P90 5,63 · max 6,40 | gemessen + A6 |
| Ladung je Besuch, obere Schranke (alle Farben, `overfull` = voll) | Median **4,35 m³** · P90 5,86 · max 6,40 | gemessen + A6 |
| Anteil Besuche mit Ladung > 6,4 m³ | **0,0 %** | gemessen + A6 |
| Volumen eines 3-Kammer-Standorts bei 100 % | **6,4 m³** (3,2 + 2,1 + 1,1) | A6/V-3, modelliert |
| Zufluss vs. Entnahme je Kammer | Anteil Zufluss > Entnahme **47,4 %** | gemessen + A6 |

### Die zwei Sackgassen (nachgerechnet)

| Ansatz | Ergebnis | Warum unbrauchbar |
|---|---|---|
| Kapazität < 6,4 m³ im Modell | Überlauf **4,91 % → ~96 %** | Das System flutet: der bilanzierte Rhythmus trägt keine Restmengen. Ist-Lauf zerstört. |
| Kapazität ≥ 6,4 m³ im Modell | **identisch** zu heute | Kein Mehrfach-Stopp je Tour belegt (Daten: ein Besuch = ein Ort). Der Parameter ist nicht unterscheidbar. |

### Belegte Spannung, die die Vorschau-Bilder zeigen sollen

Die Marktfahrzeuge fahren **3–8 Orte je Tour** (C1–C3: 23 / 29 / 31 m³ bei 4,35 m³ je Stopp).
Die Daten zeigen **einen Besuch je Ort**. Der Unterschied ist nicht die Kapazität, sondern der Takt.

> Ein Platzhalter ist damit **kein Kompromiss**, sondern die einzig wahre Abbildung des
> Wissensstandes: die Zahl ist recherchierbar, ihre Wirkung auf den Takt ist es nicht.
