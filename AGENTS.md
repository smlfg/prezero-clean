# AGENTS.md – Regeln für Coding-Agenten

Projekt: PreZero-Glascontainer, nur mit den gegebenen Daten. Fakten und Scope stehen in `README.md`.
Zahlen kommen nur aus `scripts/fakten.py`. Keine Zahl ohne Berechnung.

## 1. Daten sind die einzige Quelle
- Erlaubte Spalten: `Location_id`, `material_type`, `date`, `fill_level_perc`. Sonst nichts.
- Fehlt etwas (Koordinaten, Distanzen, Kosten, Kapazität), wird es **weggelassen**. Nicht erfinden, nicht schätzen, nicht scrapen, nicht per Zufall simulieren.
- Die CSV wird nie verändert. Abgeleitete Tabellen entstehen im Code.

## 2. Datenmodell
- **Container** = `Location_id` (449). Eine ID hat bis zu 3 Farben, die beim Leeren **gemeinsam** geleert werden.
- **Besuch** = (`Location_id`, `date`). Schlüssel. Hier wird gemessen und danach auf 0 geleert.
- **Messung** = (`Location_id`, `material_type`, `date`) mit `fill_level_perc`. Schlüssel eindeutig.
- **Füllstand** = Prozent in 10er-Stufen, `overfull` = Text, Wert unbekannt (zensiert, mindestens 100).
- **Mengen:** Messungen (11.701), Besuche (4.468), Leerungen (= Besuche, Annahme A1), Überlauf-Messungen (1.192).
- Zeit hat nur Tagesauflösung. Rate = Prozent pro Tag.

## 3. Benannte Annahmen (neue nur mit Eintrag hier)
- A1: Jeder Besuch leert alle Farben der ID auf 0.
- A2: Füllrate je Container+Farbe ist zwischen Besuchen konstant (Startwert, wird geprüft).
- A3: `overfull` = Füllstand ≥ 100 %, genauer Wert unbekannt.
Jede Annahme, die ein Ergebnis verändert, wird im Ergebnis genannt.

## 4. Bilanztest = Gate
Ein Test (`tests/test_bilanz.py`) prüft die Realität, bevor etwas anderes gebaut wird:
1. Besuche = Leerungen im Modell (Anzahl identisch zur CSV).
2. Rate × Abstand reproduziert den gemessenen Stand innerhalb eines **vorher festgelegten** Grenzwerts. Heute: mittlerer Fehler 14,4 Pp, 53 % innerhalb 10 Pp. Grenzwert legt Samuel fest, nicht der Agent.
3. Das Modell erzeugt `overfull` ungefähr so oft wie die Daten (10,2 %).
4. Backtest ohne Blick in die Zukunft: Training früher, Test später.

## 5. Die eine Zielzahl
**Eingesparte Leerungen in % gegenüber dem Ist-Plan, bei höchstens gleicher Überlaufquote.**
Ein Plan mit mehr Besuchen oder mehr Überlauf als der Ist-Plan ist kein Erfolg, egal wie schön.
Der frühere Ansatz hat Überlauf wegoptimiert und dafür deutlich mehr gefahren (Größenordnung nicht aus der CSV belegt). Das ist die falsche Richtung.

## 6. Wenn-dann-Regeln
- Wenn der Bilanztest nicht grün ist, dann **kein neues Feature**, nur Modell reparieren.
- Wenn ein Auftrag UI, Karte oder Routing verlangt, dann **ablehnen** und auf README „Nicht im Scope“ verweisen.
- Wenn eine Spalte oder Größe fehlt, dann weglassen und in einem Satz melden.
- Wenn eine Zahl in einem Text steht, dann muss sie in `fakten.py` stehen. Sonst streichen.
- Wenn ein Plan mehr Besuche braucht als der Ist-Plan, dann verwerfen.
- Wenn das Modell etwas anderes zeigt als die Daten, dann gewinnen die Daten.
- Wenn eine Annahme nötig wird, dann in Abschnitt 3 eintragen, bevor Code entsteht.

## 7. Vorgaben hinterfragen
Agenten prüfen jeden Auftrag gegen die Daten und melden Widersprüche **vor** dem Bauen. Beispiele:
- Die Daten widersprechen dem Auftrag (z. B. „alle Farben jeden Besuch“, aber nur 3.061 von 4.468 Besuchen haben alle drei).
- Der Auftrag setzt etwas voraus, das nicht in den Spalten steht.
- Der Auftrag verbessert eine Zahl, die nicht die Zielzahl ist.
Meldung: ein Satz, was nicht passt, plus ein Vorschlag. Dann auf Samuel warten.

## 8. Arbeitsweise
- Reihenfolge: Daten verstehen, Modell, Bilanztest, optimieren. Keine Phase überspringen.
- Klein halten: eine Aufgabe, eine Datei, ein Test. Pandas und Matplotlib reichen.
- Ergebnisse als Tabelle oder Diagramm mit Quelle (`fakten.py`-Abschnitt).
