# Simulations-Kino — Vertrag

Ein Artefakt, keine Evidenz. Es zeigt, wie Füllrate, Abstand und Anzahl Autos zusammenhängen.
Klar beschriftet als **Simulation**, nie als Ergebnis oder Ersparnis.

## 1. Modell (Producer / Consumer)

- **Orte:** 449 `Location_id`, je 1–3 Container (`material_type`).
- **Produzent:** Füllrate `r` in %/Tag je Container, Median aus den Daten:
  `p / Abstand zur vorigen Messung desselben Containers` (Annahmen A2 + A4).
  **Keine Saisonalität:** eine Rate je Kammer für alle Tage (A2, geprüft —
  Monats-Mediane 0,955–1,062, kein Jahresgang, `fakten.py` Abschnitt 10).
- **Konsument:** ein Auto leert einen Ort auf 0 (Annahme A1).
- **Die zwei Bilanzgrößen (Producer / Consumer) in Prozentpunkten (Pp).** Beide sind
  abgeleitet, nicht gemessen, und beide stehen als Karten im Kino:
  - **produziert** = Σ der Kammer-Raten über alle Kammern mit Rate
    (1.303 von 1.338; Median 1,52 Pp/Tag je Kammer) → **2.484,25 Pp/Tag**,
    `meta.produziert_pp_pro_tag`.
  - **abgeholt** = Σ der gemessenen Stände vor der Leerung (A5) je Tag
    (1.841,38 Pp/Tag ohne zensierte Überläufe, 2.183,91 Pp/Tag mit `overfull` = 100)
    → **2.183,91 Pp/Tag**, `meta.abgeholt_pp_pro_tag`; je Stopp **170,10 Pp**
    (`meta.abgeholt_pp_je_stopp`). Die Zahl ist eine **Untergrenze**, weil `overfull`
    zensiert ist.
  - Die Differenz (Daten: rund 300 Pp/Tag) bleibt als Füllstand im Container stehen.
    Einheit ist bewusst **Pp, keine m³ und keine Tonnen**: absolute Mengen brauchen
    externe Parameter (`AGENTS.md` §1 und §5) und sind dort parkiert.
  - Im Lauf zählt die Engine dieselben zwei Größen mit (`produziert_pp`,
    `abgeholt_pp`, `bilanz_pp`); produziert = Σ Raten × Messtage, abgeholt = Σ der
    Stände in dem Moment, in dem geleert wird.
- **Abstand `s`:** derselbe Abstand zwischen allen benachbarten Orten. Standard **5**.
  Es gibt keine Geografie, keine Koordinaten, keine Karte. `s` ist eine reine Zahl.
- **Tageskapazität:** aus den Daten ergibt sich der Ist-Durchsatz
  `K0 = 4.468 Besuche / 348 Tage = 12,83 Stopps/Tag` bei `s0 = 5`.
  Ein Auto **kann** bei Abstand `s` höchstens `K(s) = K0 * s0 / s` Stopps/Tag fahren,
  `M` Autos höchstens `K_ges = M * K(s)`. Das ist eine **Obergrenze, kein Ziel**:
  gefahren wird `min(K_ges, Bedarf)`, und der Bedarf kommt aus dem Fälligkeitsrhythmus
  (Abschnitt 2).
  - `s > s0`: die Kapazität bindet. `K(s)` fällt mit `1/s`, die Tagesstrecke ist
    `D = K0 * s0 = 64,15` Abstandseinheiten — ein größerer Abstand halbiert die Stopps,
    ohne eine erfundene Geschwindigkeit.
  - `s < s0`: der Bedarf bindet. Mehr Fahrzeit allein erzeugt keine Stopps; `s` ändert
    die Stoppzahl dann **nicht**.
  - **Modellgrenze:** `K(s) = K0 * s0 / s` unterstellt, dass je Stopp nur Fahrtzeit
    anfällt. Die feste Stoppzeit (Entladen, Rangieren) steht nicht in der CSV und ist
    deshalb nicht modelliert; dadurch ist `K(s)` für kleine `s` zu hoch. Wer sie
    einführen will, braucht eine externe Größe in `docs/externe_parameter.md`.
- **Zeit:** ein Tag = ein Schritt. Keine Uhrzeit. Keine Tonnen, keine Ladekapazität
  (steht nicht in den Daten, bleibt draußen).
- **Start:** alle Füllstände 0, **90 Tage Warmlauf**, danach 348 Tage Messfenster.
  Zählung der Metriken **erst nach dem Warmlauf**. Der Warmlauf wird beim **ersten
  Simulationsschritt** nachgeholt, nicht beim Reset: Tag 0 zeigt den leeren,
  zeitlich unveränderten Startzustand — unabhängig von Abstand `s` und Autos `M`.
  Am ersten Schritt springt die Bühne auf den Warmzustand (das ist die Simulationszeit,
  keine Darstellung).
- **Überlauf:** Füllstand **> 100 %**. Der Wert wächst weiter (A3, keine Kappung).
  In den Daten ist `overfull` zensiert; „> 100 %“ ist die nächstliegende Entsprechung.

## 2. Strategien

| Name | Regel |
|---|---|
| `ist` | Jeder Ort wird alle `p_i` Tage geleert. `p_i` = Kalibrierung des beobachteten Rhythmus (siehe unten). Das ist der bisherige Rhythmus. |
| `fuell` | Ein Ort ist fällig, wenn sein höchster Container-Füllstand ≥ `schwelle` ist. Autos bedienen die vollsten zuerst. |

**Kalibrierung des Ist-Rhythmus.** Die Median-Abstände je Ort ergeben als feste Periode
`Σ 1/gap_i` = **14,85** Fälligkeiten pro Tag — mehr als die beobachteten **12,84** Besuche pro Tag,
weil `1/gap` konvex ist und die kurzen Abstände überwiegen. Deshalb wird **ein einziger
Faktor** angewendet:

```
FAKTOR = (Σ_i 1/gap_i) / (4.468 Besuche / 348 Tage)
p_i    = gap_i * FAKTOR          (Orte mit nur einem Besuch: p_i = 348 Tage)
```

Damit verlangt der Ist-Rhythmus von sich aus genau die beobachteten 4.468 Besuche in 348 Tagen.
Der Faktor ist eine Eigenschaft der Daten, keine frei gewählte Zahl. Er wird im UI angezeigt.

**Die Abstände streuen stark** (`data/derived/orte.json`, erzeugt von `scripts/sim_daten.py`):
442 von 449 Orten haben einen Abstand, Minimum **7**, Median **33**, Maximum **172** Tage.
Der Faktor 14,85 / 12,84 = 1,157 ist deshalb vor allem eine **Korrektur der Streuung**
(Jensen: `E[1/gap] > 1/E[gap]`), nicht eine Eigenschaft eines Fahrzeugs. Folge für
Abschnitt 1: `K0` ist ein **Durchsatz aus einer streuenden Abstandsverteilung** und
damit keine gemessene Kapazität — die Kapazitätsaussage ist gesetzt, nicht gemessen.

**Startversatz.** Der erste Fälligkeitstermin des Ortes `i` liegt bei `i * p_i / n`.
Er ist eine reine Startbedingung (kein Datenwert) und wird nicht als Zahl ausgegeben.

## 3. Metriken (live, je Lauf)

- **Produziert / Abgeholt** (Pp/Tag, laufend und über den Lauf) — die Bilanz aus
  Abschnitt 1, plus **Bilanz** = produziert − abgeholt.
- **Leerungen** (Stopps) — die Kosteneinheit.
- **Überlauf-Tage** (Ort-Tage mit Füllstand ≥ 100).
- **Überlauf bei Leerung** (Anteil der Stopps, bei denen ein Container ≥ 100 war).
- **Ø Füllstand** (ohne zensierte Überläufe, wie in `fakten.py`).
- **Distanz** = `s × Stopps` (nur die angefahrenen Stopps).
- **Auslastung** = bediente / fällige Stopps.
- **Kapazität/Tag** = `M · K(s)` — Obergrenze, kein Ziel. **Bedarf/Tag** = fällige
  Stopps pro Tag. Gelesen wird `min(Kapazität, Bedarf)`: liegt der Bedarf darunter,
  ist `s` wirkungslos.

Immer **gegen den Ist-Lauf im selben Panel**, nie absolut allein.

## 4. Datenschnittstelle `data/derived/orte.json`

```json
{
  "meta": {
    "erzeugt": "2026-11-16T...",
    "quelle": "data/raw/glass_fill_levels_anonymized_f.csv",
    "skript": "scripts/sim_daten.py",
    "orte": 449,
    "container": 1338,
    "messungen": 11701,
    "besuche": 4468,
    "tage": 348,
    "k0_pro_tag": 12.8,
    "s0": 5.0,
    "produziert_pp_pro_tag": 2484.25,
    "produziert_kammern": 1303,
    "produziert_pp_pro_tag_kammer_median": 1.52,
    "abgeholt_pp_pro_tag": 2183.91,
    "abgeholt_pp_je_stopp": 170.1
  },
  "orte": [
    {
      "id": "c1a14cc5-fcdd-4abe-9ef6-a4d62630c065",
      "gap": 26.0,
      "container": [
        {"farbe": "brown", "rate": 0.52, "n": 12},
        {"farbe": "green", "rate": 1.10, "n": 14},
        {"farbe": "white", "rate": 1.42, "n": 15}
      ]
    }
  ]
}
```

Regeln für den Export:
- `rate` = Median aus numerischen Folgemessungen (`p / tage`), nur `p > 0` und `tage > 0`.
- Container ohne verwertbare Rate bekommen `rate = null` und werden vom Kino mit `0` behandelt,
  aber **gezählt und im `meta` ausgewiesen** (`container_ohne_rate`).
- `gap` = Median der Besuchsabstände des Ortes, `null` bei nur einem Besuch.
- Keine Zahl von Hand. Alles aus der CSV.

## 5. UI (das Kino)

- **Oben:** Abstand `s` (2,5–20, Schritt 0,5) · Autos `M` (1–4) · Strategie (`ist`/`fuell`)
  · **Ansicht (`ringe`/`container`, Standard `ringe`)** · Schwelle (50–95 %, nur bei `fuell`)
  · Play/Pause · Tempo · Tag-Anzeige.
- **Kalender (unter der Steuerleiste):** die Simulationstage als Raster — **eine Zelle = ein
  Tag**, eine Zeile = 7 Tage (Woche), ein Block = ein Zwölftel des Messfensters (bei 348 Tagen
  **29 Tage** je Monat). Gelaufene Tage sind gefüllt, der aktuelle Tag ist hervorgehoben, die
  übrigen bleiben leer. Reine Darstellung (`S`): **kein Kalenderdatum**, keine Wochentage,
  keine Prognose für echte Kalendertage. Die Daten haben nur Tagesauflösung; der Kalender
  zählt Simulationstage und erfindet keine Datumsangabe.
- **Tagesbewertung (Farbe der Zelle):** `gedeckt` = alle **fälligen Stopps des Tages** wurden
  bedient; `verpasst` = mindestens ein fälliger Stopp blieb offen (Rückstau, die Kapazität
  reichte nicht). Bedarf (`fällig`) und Abdeckung (`bedient`) stehen je Tag im
  `tagesverlauf` der Engine und sind Modellgrößen (`S`). Der Überlauf bewertet den Tag **nicht**
  mit: er liegt an jedem Tag vor und hat seine eigene Kurve im Verlauf darunter.
- **Bühne, Ansicht `ringe`:** drei konzentrische Ringe, außen → innen **Weiß (448), Grün (448),
  Braun (442)**. Jeder Ort `i` liegt auf allen Ringen beim selben Winkel `i·2π/449 − π/2`;
  die Kammern einer ID fluchten radial („Zuordnung über ID"). Fehlt einem Ort eine Farbe,
  bleibt an diesem Winkel eine Lücke. Jedes Farbband hat eine **Tiefe** — sie nimmt den
  Raum, der bisher leer zwischen den Ringen lag. Das **Grundband** in der Glasfarbe zeigt,
  wo eine Kammer existiert; darüber liegt der **Keil** der Kammer mit **fester Grundlinie**:
  er beginnt am Innenrand des Bandes und ist `Füllstand/100 · Bandtiefe` lang. Eine leere
  Kammer hat keinen Keil, nur das Grundband; eine fehlende Kammer bleibt eine Lücke. Über
  100 % ist die Länge gedeckelt — den Überlauf trägt allein der rote Rand am Außenrand des
  Bandes. Damit kodiert die **Länge** den Füllstand (in Graustufen lesbar), die Farbe
  zusätzlich (leer → voll → übervoll). Bandtiefe, Grundband und Keil sind Darstellung (`S`).
- **Bühne, Ansicht `container`:** ein Ort = ein Container mit drei radial gestapelten Kammern
  (außen Weiß, Mitte Grün, innen Braun), verbunden durch eine feine Linie. Winkel und
  Füllstandskodierung sind identisch zu `ringe` (Grundband + Keil, nur mit kleinerer
  Bandtiefe); fehlt eine Kammer, bleibt sie leer. Damit
  wird sichtbar, dass die Farben zusammen **einen** Container bilden (Rahmen bleibt stehen,
  Kammern werden einzeln geleert) — wie beim realen Mehrkammer-Depotcontainer.
- **Beide Ansichten:** Autos auf einer dünnen Spur außerhalb der Bühne; beim Leeren ein
  kurzer radialer Blitz an der besuchten ID. Ringreihenfolge, Farben, Kammerabstand und
  Ansicht sind Darstellung (`S`), keine Daten; die Simulation selbst bleibt unverändert.
- **Unten:** die Kennzahlen live, plus Verlauf als **zwei Panels** mit gemeinsamer
  x-Achse „Tag“ (nur sie ist beschriftet) und je eigener y-Skala. Getrennt, weil zwei
  Einheiten in einem Bild einen Vergleich vortäuschen, den es nicht gibt.
- **Fußzeile:** „Simulation — keine Messung. Raten und Rhythmus aus den Daten, alles andere Annahme."

Verboten: Karte, Koordinaten, km, Euro, Tonnen, Prognose für echte Kalendertage.
Der Ist-Lauf ist immer daneben sichtbar; ohne Vergleich keine Zahl.

## 6. Abnahme

1. Default (`s=5`, `M=1`, `ist`) erzeugt ungefähr so viel Überlauf wie die Daten (~10 %).
   **Ist-Stand: 4,91 % Überlauf-Quote, 4.407 Leerungen** (Daten: 10,19 %, 4.468 Besuche).
   Der Ist-Lauf erzeugt also **weniger** Überlauf als die Daten, nicht mehr. Das war schon
   vor der Herkunftsmarkierung so (gegen `HEAD` geprüft) und ist **keine** Regression,
   sondern ein offener Punkt des Modells: der Ist-Rhythmus ist über die Kalibrierung
   auf die *Anzahl* der Besuche festgelegt, nicht auf die *Überlaufquote*. Wer die
   Quote angleichen will, muss das im Modell entscheiden, nicht in der Anzeige.
2. `s` verdoppeln halbiert die Stopps pro Tag, **solange die Kapazität bindet** (`s ≥ s0`).
   (Ist: 12,7 → 6,4 Stopps/Tag.) Für `s < s0` bleibt die Stoppzahl konstant, weil der
   Bedarf bindet — das ist kein Fehler, sondern die Modellgrenze aus Abschnitt 1.
3. `M` erhöhen senkt oder hält den Überlauf.
4. Deterministisch: gleicher Seed, gleicher Lauf, gleiche Zahlen.
5. Referenz: eine unabhängige Python-Implementierung liefert für einen festen Parametersatz
   dieselben Metriken wie die Seite (Toleranz ±1 Stopp, ±0,5 Pp).
   (Ist: über alle fünf Läufe Diff 0.)
6. Herkunftsmarkierung: jede sichtbare Zahl trägt einen Marker aus Abschnitt 7.
   Ein Marker wird nie ohne Klartext-Beispiel ausgegeben.

## 7. Herkunftsmarkierung

Jede sichtbare Zahl im Kino trägt einen Marker. **Drei Kategorien, mehr nicht.**

| Marker | Kategorie | Definition | Beispiel |
|---|---|---|---|
| `M` | **gemessen** | steht so in der CSV | 11.701 Messungen · 4.468 Besuche · 45,5 % voll bei Leerung |
| `A` | **abgeleitet** | aus Messwerten berechnet, **keine** Annahme | Rate je Kammer · 12,8 Stopps/Tag · Kalibrierungsfaktor 1,1565 |
| `S` | **gesetzt** | Annahme, Modellgröße, Startwert oder Darstellung | `s` = 5 · `M` = 1 · Warmlauf 90 Tage · Ringreihenfolge |

Die Grenze zwischen `M` und `A`: **gemessen** ist der Wert selbst, **abgeleitet** ist eine
Rechnung auf gemessenen Werten. Der Kalibrierungsfaktor 1,1565 ist abgeleitet, nicht
gemessen — er entsteht erst aus `Σ 1/gap` gegenüber 4.468/348. Der Füllstand einer Kammer
ist im Kino abgeleitet (Median aus Folgemessungen), nicht gemessen, weil er im Lauf
fortgeschrieben wird.

Die **Tageskapazität** (`M · K(s)`) trägt `S`, nicht `A`: sie enthält das gesetzte `s0`
und den gesetzten Abstand `s` und ist damit eine Modellgröße. `K0` allein bleibt `A`
(4.468 / 348 aus der CSV).

### 7.1 Quelle der Marker

Die Marker stehen **nicht** im HTML. Sie kommen aus `meta.herkunft` in
`data/derived/orte.json`, erzeugt von `scripts/sim_daten.py`:

- `meta.herkunft.kategorien` — Code, Kurzname und Klartext je Kategorie
- `meta.herkunft.meta` — Herkunft jeder Größe aus dem `meta`-Block
- `meta.herkunft.sonstige` — Herkunft der Größen, die nicht im `meta`-Block stehen

Das Kino liest diese Tags und setzt die Chips. **Kein Chip steht von Hand im HTML.**
Damit können Dokument und Seite nicht auseinanderlaufen.

### 7.2 Wo welcher Marker sitzt

| Element | Marker | Grund |
|---|---|---|
| Kopfzeile: Orte, Kammern | `M` | direkt aus der CSV |
| Kopfzeile: Ringreihenfolge, „alle Abstände gleich" | `S` | Darstellung |
| Steuerleiste: Abstand `s`, Autos `M`, Strategie, Schwelle, Lauf, Tempo | `S` | Modellgrößen und Startwerte |
| Steuerleiste: „Stopps/Tag" | `A` | aus Besuchen und Tagen gerechnet |
| Kalender: Tagesraster, Wochenzeilen, Monatsblöcke | `S` | Darstellung; ein Monat = 29 Simulationstage, kein Kalenderdatum |
| Kalender: gefüllte Tage und hervorgehobener aktueller Tag | `S` | Modellzeit dieses Laufs |
| Kalender: Tagesbewertung `gedeckt`/`verpasst` | `S` | Modellrechnung: fällige Stopps vs. bediente Stopps des Tages |
| Bühne: Füllstand der Kammer | `A` | Median aus Folgemessungen, im Lauf fortgeschrieben |
| Bühne: Ringreihenfolge, Farben, Lage der Orte | `S` | reine Darstellung |
| Kennzahlenkarten: alle Laufwerte | `S` | Modellrechnung dieses Laufs |
| Kennzahlenkarten: „Produziert (Producer)" und „Abgeholt (Consumer)" | `S` | Laufwerte aus Raten × Messtage bzw. Σ Stände bei Leerung |
| Kennzahlenkarten: die Vergleichszahlen zu Producer/Consumer | `A` | `meta.produziert_pp_pro_tag`, `meta.abgeholt_pp_pro_tag`, `meta.abgeholt_pp_je_stopp` |
| Kennzahlenkarten: Vergleichswerte aus den Daten | `M` bzw. `A` | je nach Größe aus `meta.herkunft` |
| Kennzahlenkarten: „Differenz produziert − abgeholt" | `S` | Modellrechnung (`bilanz_pp`), steht als Satz in der Consumer-Karte |
| Verlauf: zwei Panels, Kurven und y-Skalen | `S` | Modellrechnung dieses Laufs |
| Verlauf oben: gestrichelte Ist-Linie | `M` | gemessene Besuchszahl (`meta.besuche`) als Bezug der Zielzahl |
| Verlauf unten: **keine** Ist-Linie | `—` | die Daten kennen keinen Überlauf-Tag; eine Linie wäre eine erfundene Annahme |
| Verlauf: x-Achsbeschriftung, Raster, Skalenwahl | `S` | Darstellung; die y-Achse bleibt unbeschriftet |
| Fußzeile: Messungen, Orte, Kammern, Besuche, Tage | `M` | direkt aus der CSV |

### 7.3 Regeln

- Keine Zahl im Kino ohne Marker. Ausnahme: Achsen- und Ringbeschriftungen; die stehen
  in Bereichen, die als `S` ausgewiesen sind.
- Die Legende nennt je Kategorie ein **Klartext-Beispiel mit echten Werten** aus `meta`.
- Marker ändern **keine** Werte. Sie markieren Herkunft, sonst nichts.
- Eine neue Größe im Kino braucht einen Eintrag in `meta.herkunft`; ohne Eintrag
  greift `S` und die Größe gilt als gesetzt.
- Der Zeitstempel `meta.erzeugt` und der Quellpfad der CSV sind keine Zahlen und
  tragen keinen Marker.

### 7.4 Keine Zahl steht an zwei Orten

`K0` (Ist-Durchsatz) und `S0` (Ausgangsabstand) lagen früher fest verdrahtet in
`sim/engine.js`, `scripts/sim_referenz.py` und im HTML. Sie stehen jetzt **ausschließlich**
in `meta` (`k0_pro_tag`, `s0`) und werden überall von dort gelesen. Neue Zahlen
gehören nach `meta`, nicht in den Code.

### 7.5 Testbarkeit

Die Seite schreibt ihren Zustand zusätzlich in das Element `#simWerte` (JSON mit
`params` und `metrics`). Das ist nötig, weil Browser-Erweiterungen ihren Prüfcode in
einer isolierten Welt ausführen, in der `window.simFinish` nicht sichtbar ist — das
DOM ist der einzige gemeinsame Ort. Der Wert wird bei jeder Änderung aktualisiert:
nach `simSet`/`simFinish` sofort, im Lauf bei jedem neuen Tag (Kennzahlen und Verlauf
hängen am Tag, nicht am Frame — ein Frame ohne neuen Tag schreibt keine Zahl neu).

```
window.simSet({s: 10, m: 2})   // Parameter setzen
document.getElementById("simWerte").textContent   // Zustand als JSON
```

