# Simulations-Kino — Vertrag

Ein Artefakt, keine Evidenz. Es zeigt, wie Füllrate, Abstand und Anzahl Autos zusammenhängen.
Klar beschriftet als **Simulation**, nie als Ergebnis oder Ersparnis.

## 1. Modell (Producer / Consumer)

- **Orte:** 449 `Location_id`, je 1–3 Container (`material_type`).
- **Produzent:** Füllrate `r` in %/Tag je Container, Median aus den Daten:
  `p / Abstand zur vorigen Messung desselben Containers` (Annahmen A2 + A4).
- **Konsument:** ein Auto leert einen Ort auf 0 (Annahme A1).
- **Abstand `s`:** derselbe Abstand zwischen allen benachbarten Orten. Standard **5**.
  Es gibt keine Geografie, keine Koordinaten, keine Karte. `s` ist eine reine Zahl.
- **Tagesleistung:** aus den Daten ergibt sich der Ist-Durchsatz
  `K0 = 4.468 Besuche / 348 Tage = 12,83 Stopps/Tag` bei `s0 = 5`.
  Ein Auto schafft bei Abstand `s`: `K(s) = K0 * s0 / s` Stopps/Tag.
  `M` Autos: `K_ges = M * K(s)`.
  Damit ist die Tagesstrecke eines Autos konstant `D = K0 * s0 = 64,15` Abstandseinheiten;
  ein größerer Abstand halbiert die Stopps, statt eine erfundene Geschwindigkeit zu brauchen.
- **Zeit:** ein Tag = ein Schritt. Keine Uhrzeit. Keine Tonnen, keine Ladekapazität
  (steht nicht in den Daten, bleibt draußen).
- **Start:** alle Füllstände 0, **90 Tage Warmlauf**, danach 348 Tage Messfenster.
  Zählung der Metriken **erst nach dem Warmlauf**.
- **Überlauf:** Füllstand **> 100 %**. Der Wert wächst weiter (A3, keine Kappung).
  In den Daten ist `overfull` zensiert; „> 100 %“ ist die nächstliegende Entsprechung.

## 2. Strategien

| Name | Regel |
|---|---|
| `ist` | Jeder Ort wird alle `p_i` Tage geleert. `p_i` = Kalibrierung des beobachteten Rhythmus (siehe unten). Das ist der bisherige Rhythmus. |
| `fuell` | Ein Ort ist fällig, wenn sein höchster Container-Füllstand ≥ `schwelle` ist. Autos bedienen die vollsten zuerst. |

**Kalibrierung des Ist-Rhythmus.** Die Median-Abstände je Ort ergeben als feste Periode
`Σ 1/p_i` = **16,1** Fälligkeiten pro Tag — mehr als die beobachteten **12,83** Besuche pro Tag,
weil `1/gap` konvex ist und die kurzen Abstände überwiegen. Deshalb wird **ein einziger
Faktor** angewendet:

```
FAKTOR = (Σ_i 1/gap_i) / (4.468 Besuche / 348 Tage)
p_i    = gap_i * FAKTOR          (Orte mit nur einem Besuch: p_i = 348 Tage)
```

Damit verlangt der Ist-Rhythmus von sich aus genau die beobachteten 4.468 Besuche in 348 Tagen.
Der Faktor ist eine Eigenschaft der Daten, keine frei gewählte Zahl. Er wird im UI angezeigt.

**Startversatz.** Der erste Fälligkeitstermin des Ortes `i` liegt bei `i * p_i / n`.
Er ist eine reine Startbedingung (kein Datenwert) und wird nicht als Zahl ausgegeben.

## 3. Metriken (live, je Lauf)

- **Leerungen** (Stopps) — die Kosteneinheit.
- **Überlauf-Tage** (Ort-Tage mit Füllstand ≥ 100).
- **Überlauf bei Leerung** (Anteil der Stopps, bei denen ein Container ≥ 100 war).
- **Ø Füllstand** (ohne zensierte Überläufe, wie in `fakten.py`).
- **Distanz** = `s × Stopps`.
- **Auslastung** = bediente / fällige Stopps.

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
    "s0": 5.0
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
- **Bühne, Ansicht `ringe`:** drei konzentrische Ringe, außen → innen **Weiß (448), Grün (448),
  Braun (442)**. Jeder Ort `i` liegt auf allen Ringen beim selben Winkel `i·2π/449 − π/2`;
  die Kammern einer ID fluchten radial („Zuordnung über ID"). Fehlt einem Ort eine Farbe,
  bleibt an diesem Winkel eine Lücke. Der Grundring zeigt die Glasfarbe, das Segment darüber
  den Füllstand (leer → voll → übervoll, roter Rand ab 100 %).
- **Bühne, Ansicht `container`:** ein Ort = ein Container mit drei radial gestapelten Kammern
  (außen Weiß, Mitte Grün, innen Braun), verbunden durch eine feine Linie. Winkel und
  Füllstandskodierung sind identisch zu `ringe`; fehlt eine Kammer, bleibt sie leer. Damit
  wird sichtbar, dass die Farben zusammen **einen** Container bilden (Rahmen bleibt stehen,
  Kammern werden einzeln geleert) — wie beim realen Mehrkammer-Depotcontainer.
- **Beide Ansichten:** Autos auf einer dünnen Spur außerhalb der Bühne; beim Leeren ein
  kurzer radialer Blitz an der besuchten ID. Ringreihenfolge, Farben, Kammerabstand und
  Ansicht sind Darstellung (`S`), keine Daten; die Simulation selbst bleibt unverändert.
- **Unten:** die sechs Metriken live, plus Sparkline „Überlauf-Tage pro Tag".
- **Fußzeile:** „Simulation — keine Messung. Raten und Rhythmus aus den Daten, alles andere Annahme."

Verboten: Karte, Koordinaten, km, Euro, Tonnen, Prognose für echte Kalendertage.
Der Ist-Lauf ist immer daneben sichtbar; ohne Vergleich keine Zahl.

## 6. Abnahme

1. Default (`s=5`, `M=1`, `ist`) erzeugt ungefähr so viel Überlauf wie die Daten (~10 %).
2. `s` verdoppeln halbiert die Stopps pro Tag.
3. `M` erhöhen senkt oder hält den Überlauf.
4. Deterministisch: gleicher Seed, gleicher Lauf, gleiche Zahlen.
5. Referenz: eine unabhängige Python-Implementierung liefert für einen festen Parametersatz
   dieselben Metriken wie die Seite (Toleranz ±1 Stopp, ±0,5 Pp).
