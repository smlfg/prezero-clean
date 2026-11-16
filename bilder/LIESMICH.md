# Bilder — Arbeitsstand der Diagnose

Erzeugt von `scripts/bilder.py` aus `data/raw/glass_fill_levels_anonymized_f.csv`.
Keine Zahl ist von Hand eingetragen. Regeln: `assets/ui/UI_REGELN.md`.

```bash
.venv/bin/python scripts/bilder.py
```

Das sind **Diagnose-Bilder**, nicht das Befund-Blatt. Sie zeigen nur, was in den Daten steht.
Es gibt noch kein Modell, keinen Plan und keinen Bilanztest — deshalb fehlt auch die Zielzahl.

---

## 01_mechanismus.png — ein Ort, drei Farben

**Aussage:** Derselbe Besuch ist für Braun zu früh und für Weiß zu spät.

Ort `c1a14cc5…` (deterministisch gewählt: drei Farben, je ≥ 12 Ablesungen, größte Spanne).
Braun liegt im Mittel bei 22 %, Grün bei 66 %, Weiß bei 87 %. Jeder Punkt ist eine Ablesung,
gepunktet sind Leerung auf 0 (Annahme A1) und Wiederanstieg (Annahme A2).
Zwischen zwei Ablesungen wurde nichts gemessen.

**Nicht gezeigt:** was in der Zeit zwischen zwei Besuchen wirklich passiert.

---

## 02_alle_orte.png — 449 Orte ohne Karte

**Aussage:** Die Orte unterscheiden sich extrem. Ein Takt für alle kann für keinen richtig sein.

Jeder Strich ist ein Ort, Länge = Median-Füllstand bei der Ablesung, Punkt = Anteil overfull.
Sortiert nach diesem Median. Die Reihenfolge ist ein Datenwert, keine Lage.
Median über alle Orte: 65 %. `overfull` zählt als 100 % (zensiert).

**Nicht gezeigt:** keine Geografie, keine Nähe, keine Route. Absicht.

---

## 03_einheit.png — dieselben Daten, zwei Einheiten

**Aussage:** Die Einheit entscheidet, welche Geschichte man erzählt.

Je Ablesung (Container + Farbe): Braun 70 % unter 50 %, Weiß 16 % übervoll.
Je Besuch (vollste Farbe): 8 % / 47 % / 45 %. Der Unterschied entsteht, weil ein Besuch
drei Farben gleichzeitig trifft.

**Nicht gezeigt:** dass eine der beiden Einheiten falsch wäre. Beide sind richtig, sie beantworten
verschiedene Fragen. Deshalb steht die Einheit ab jetzt neben jeder Zahl.

---

## 04_takt.png — länger warten füllt nicht mehr

**Aussage:** Der Füllstand bei der Ablesung steigt bis etwa 15–30 Tage und bleibt dann flach.
Der Überlauf steigt weiter: 1,0 % bei ≤ 7 Tagen, 16,6 % bei > 60 Tagen.

Der Mittelwert ist **ohne** `overfull` gerechnet. Das ist der Grund, warum er flach wird:
Je voller ein Container, desto wahrscheinlicher fällt er aus dem Mittel heraus.
Der Überlauf-Anteil zeigt, was der Mittelwert verdeckt.

**Nicht gezeigt:** dass ein längerer Takt besser wäre. Dafür fehlt das Modell.

---

## Was hier bewusst fehlt

- **Die Tauschkurve** (Leerungen gegen Überlaufquote, Ist-Punkt und Plan-Punkt). Sie braucht
  einen Plan, und den gibt es noch nicht.
- **Die eine Zielzahl** (eingesparte Leerungen bei höchstens gleicher Überlaufquote). Sie braucht
  den Bilanztest.
- **Alles mit Raum:** Karte, km, Euro, Tour, Gebiet, Fahrzeug, Kapazität.

Solange der Bilanztest nicht grün ist, bleibt es bei diesen vier Bildern.
