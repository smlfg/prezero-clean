# UI-Regeln — „was zum sehen“ (Befund-Blatt, keine App)

Geltung: bindend für jedes Bild, Diagramm oder HTML in diesem Repo.
Diese Datei **erlaubt kein UI** (siehe `SCOPE.md`, „Nicht im Scope“). Sie begrenzt die eine Ausnahme:
ein statisches Befund-Blatt, das den Befund zeigt.

Leitsatz: **Ein Bild, das eine Annahme braucht, ist keine Evidenz.**

---

## 0. Der eine Satz, den das Bild sagen muss

> „Zu früh geleert kostet Leerungen. Ein Plan nach Füllstand spart Leerungen, ohne mehr Überlauf.“

Wenn das Bild diesen Satz nicht in 10 Sekunden stützt, ist es das falsche Bild.

---

## 1. Raum — der wichtigste Block

Jeder Abstand ist gleich. Raum ist damit eine Konstante und hat im Bild nichts zu suchen.

**Muss**
- Orte als theoretische Plätze behandeln: `Location_id` ohne Adresse, ohne Lage.
- Orte beliebig anordnen — und zwar nach einer **Daten**-Eigenschaft (Füllrate, Überlaufhäufigkeit), nie nach Geografie.
- Die Sortierung im Bild benennen: „sortiert nach Füllrate, absteigend“.
- Kosten in Stopps rechnen. `km = c × Stopps`, also ist die Stoppzahl die einzige Größe.

**Darf nicht**
- Karte, Koordinaten, Standort-Pins, Kacheln, Zoom, Pan.
- km, Distanz, Fahrzeit, Euro, CO₂, Kraftstoff, Tonnen.
- „Gebiet“, Cluster, Nachbarschaft, Nähe, Region.
- Tour, Route, Reihenfolge, Fahrzeug, Schicht, Kapazität.
- irgendetwas, das nach Stadt aussieht.

**Warum:** Unter gleichen Abständen ist „ich fahr da eh vorbei“ gratis. Die Verschwendung ist reines
Timing. Jede Ortsdarstellung lädt genau die Frage ein, die man nicht beantworten kann.

---

## 2. Zeit

Zeit ist die einzige Variable. Das Bild braucht eine Zeitachse, keine Ortsachse.

**Muss**
- Messpunkte als Punkte zeichnen. Zwischen zwei Messungen ist **nichts** bekannt.
- `overfull` als Bereich „≥ 100 %, Wert unbekannt“ darstellen (Band, Pfeil, offener Balken). Nicht als 100, nicht als 110.
- 10er-Stufen sichtbar lassen (Treppe, keine glatte Kurve).
- Jeden Besuch als Ereignis markieren (Tropfen/Linie) und in eine Klasse färben:
  **zu früh · passt · übervoll**.
- Die drei Klassengrenzen vorher festlegen und im Bild nennen.
- Tagesauflösung respektieren. Keine Stunden, keine Zwischenwerte.

**Darf nicht**
- Prognose, Forecast, „+7/+14/+21 Tage“, Trendlinie in die Zukunft.
- Interpolation, Glättung, Spline, „wahrscheinlicher Verlauf“.
- Jahres-Heatmap mit geschätzten Wiederanstiegen.
- eine Kurve, die kontinuierliche Messung suggeriert.

**Warum:** Jede geglättete Linie behauptet Wissen zwischen zwei Fahrer-Schätzungen. Das war der
Punkt, an dem die alten Zahlen angreifbar wurden.

---

## 3. Zahlen

**Muss**
- Jede Zahl aus `scripts/fakten.py`, ein Lauf, ein Commit, ein Datum.
- Quellenzeile unter jedem Bild: Skript, Datensatz, Zeitraum, n.
- Ist-Basis immer daneben: 4.468 Besuche, 10,2 % Überlauf-Messungen.
- Die eine Zielzahl allein und groß: **eingesparte Leerungen in % bei höchstens gleicher Überlaufquote**.
- Beide Seiten eines Vergleichs in derselben Einheit (Leerungen vs. Leerungen, % vs. %).

**Darf nicht**
- handgetippte Zahlen, „ca.“, „rund“, aus einer Folie übernommen.
- Mittelwerte, die die Klassen verdecken (das „Ø Füllstand %“-Muster).
- eine Teiltour gegen „alles leeren“ vergleichen (25 von 127).
- zwei Zeiträume, zwei Modelle oder zwei Grundgesamtheiten in einem Bild mischen.
- eine Zahl ohne Einheit, ohne n, ohne Zeitraum.

**Harte Regel:** Braucht der Plan **mehr** Leerungen als der Ist-Plan, ist das Bild **rot** —
kein Erfolg, keine Ausnahme, keine schönere Achse.

---

## 4. Darstellung

**Muss**
- Ein Bild = eine Aussage. Zwei Aussagen = zwei Bilder.
- Höchstens drei Bilder, in dieser Reihenfolge:
  1. **Mechanismus:** ein Ort über die Zeit, Besuche und Klassen.
  2. **Verteilung:** alle Orte untereinander (Zeilen = Orte, Spalten = Zeit), sortiert.
  3. **Tauschkurve:** Besuche gegen Überlaufquote, Ist-Punkt markiert, Plan als zweiter Punkt.
- Statisch: PNG oder HTML **ohne JavaScript**.
- Festes Format: 1600×900 oder eine A4-Seite. Kein „responsiv“.
- Direkt beschriftete Linien und Punkte statt Legende.
- Drei Farben für drei Zustände, über alle Bilder gleich; zusätzlich Form/Schraffur, damit es in Graustufen lesbar bleibt.
- Eine Datumszeile unter dem Titel. Nicht mehr.

**Darf nicht**
- Tabs, Rollen, Navigation, Sprunglinks, Filter, Dropdowns, Slider.
- Datums-Wähler, Upload, Freigabe-Workflow, Copilot, Suche.
- KPI-Karten, Header, Logo, Dashboard-Rahmen.
- Hover, Tooltip, Animation, Autoplay.
- Badges („Stand …“) auf jeder Karte — eine Zeile reicht.
- eine Interaktion, die man braucht, um das Bild zu verstehen.

**Test:** Wenn ein Klick nötig ist, ist es wieder UI.

---

## 5. Prozess

**Muss**
- Reihenfolge: Daten → Modell → **Bilanztest grün** → erst dann das Bild.
- Das Bild ist die Belohnung, nicht die Arbeit.
- Neue Bildart nur mit Eintrag in dieser Datei (wie neue Annahmen in `AGENTS.md` §3).
- Ein Bild, ein Skript, ein Lauf. Reproduzierbar mit einem Befehl.

**Darf nicht**
- ein Bild bauen, um ein Modell zu retten.
- das Bild „fertig“ nennen, solange der Bilanztest rot ist.
- in der Nacht vor der Abgabe Farben, Badges oder Layout polieren.
- eine Zahl im Bild ändern, ohne das Skript zu ändern.

---

## 6. Sprache

**Muss**
- Den Mechanismus benennen: „zu früh geleert“, „läuft über“, „Takt passt“.
- Den Stakeholder-Satz aufgreifen: „Gebiet für Gebiet spart keinen Meter, es kostet Leerungen.“
- Unsicherheit aussprechen, wo sie ist: `overfull` ist zensiert, Zeit hat nur Tagesauflösung.

**Darf nicht**
- „Optimierung“, „KI“, „Prognose“, „smart“, „digital“, „Plattform“.
- „bis zu“, „potenziell“, „theoretisch möglich“ als Zahlenverstärker.
- eine Ersparnis in % ohne die Vergleichsbasis im selben Satz.
- „simuliert“ erklären müssen. Was eine Erklärung braucht, fliegt raus.

---

## 7. 10-Sekunden-Test (vor jeder Abgabe)

1. Sagt ein Fremder nach 10 Sekunden, was das Problem ist? (ohne dich)
2. Ist jede Zahl mit einem Befehl nachrechenbar?
3. Braucht irgendein Element eine Annahme, die nicht im Bild steht?
4. Ist irgendwo eine Karte, eine km-Angabe, ein Euro-Betrag?
5. Muss man klicken, scrollen oder umschalten?
6. Steht die eine Zielzahl allein und mit Vergleichsbasis?
7. Ist der Plan bei gleicher Überlaufquote **besser** — oder nur schöner?

Eine „nein“ bei 1–3 oder 6–7, ein „ja“ bei 4–5: nicht abgeben.

---

## 8. Hackathon-Antimuster → Regel

| Was damals passiert ist | Verstoß | Regel heute |
|---|---|---|
| 11 Tabs, 35 MB HTML, Karte, Copilot, A/B-Replay | Produkt statt Beweis | Ein Blatt, max. 3 Bilder, kein JS |
| Koordinaten simuliert, Haversine, km, Tonnen, Euro | erfundene Genauigkeit | Raum ist konstant, fällt raus |
| „81 %“ zurückgezogen, „83,4 %“ Teiltour | Zahl ohne Basis | Zielzahl nur mit Ist-Basis daneben |
| Szenario mit 15.976 statt 10.363 Leerungen als „günstigste“ | falsches Ziel optimiert | mehr Leerungen = rot |
| Stunden für „Stand“-Badges und tote Tab-Links | Politur statt Modell | eine Datumszeile, keine Navigation |
| Prognose +7/+14/+21 in der Oberfläche | Wissen behauptet | nur Messpunkte, keine Zukunft |
| „Was echt ist und was simuliert wird“ als Kapitel | Elemente, die eine Erklärung brauchen | was erklärt werden muss, fliegt raus |
