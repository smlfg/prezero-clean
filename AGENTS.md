# AGENTS.md – Regeln für Coding-Agenten

Projekt: PreZero-Glascontainer, nur mit den gegebenen Daten. Fakten und Scope stehen in `README.md`.
Zahlen kommen nur aus `scripts/fakten.py`. Keine Zahl ohne Berechnung.

## 1. Daten und externe Parameter strikt trennen
- **Interne beobachtete Variablen** stammen ausschließlich aus `data/raw/glass_fill_levels_anonymized_f.csv` und dürfen nur die Spalten `Location_id`, `material_type`, `date`, `fill_level_perc` verwenden. Daraus eindeutig abgeleitete Größen (z. B. Besuchsabstand, Füllrate, Überlaufquote) bleiben ebenfalls intern; ihr Herkunftsstatus wird im Ergebnis benannt.
- **Externe Variablen** (z. B. Containervolumen, Kammeranzahl, Materialdichte, tatsächliches Volumen hinter `overfull`) sind nicht in der CSV beobachtet. Sie dürfen nur durch belastbare externe Primärquellen ergänzt werden, niemals erfunden, geschätzt oder per Zufall simuliert. Sie werden getrennt von den internen Fakten mit Wert, Einheit, Geltungsbereich, Quelle, Abrufdatum und Unsicherheit dokumentiert.
- Fehlt eine interne Größe (z. B. Koordinaten, Distanzen, Kosten, Kapazität), wird sie **weggelassen**. Fehlt nur der externe Wert, bleibt die interne Analyse zulässig; eine daraus abgeleitete absolute Mengenaussage wird erst nach dokumentierter externer Belegung ausgegeben.
- Die CSV wird nie verändert. Abgeleitete Tabellen entstehen im Code.
- **Begriffskonvention in Berichten, Code und Ergebnissen:** „gemessen“ = direkt aus der CSV; „abgeleitet“ = aus internen Beobachtungen berechnet; „modelliert“ = Ergebnis einer benannten Annahme; „recherchiert“ = externer Parameter mit Quelle und Unsicherheit; „geplant“/„optimiert“ = Ergebnis des neuen Besuchsplans. Statistikschätzungen werden als „geschätzt“ bezeichnet.
- Absolute Mengen werden aus internem Füllstand und externer Kapazität ausschließlich als Sensitivity-Ergebnis berechnet: `Volumen = Füllstand_prozent / 100 * Kammervolumen`. Bandbreite und verwendete Annahme sind immer mitanzugeben; nie als exakte CSV-Wahrheit darstellen. Externe Parameter mit Quelle und Unsicherheit: `docs/externe_parameter.md` (V-1 Bandbreite 0,53/1,07/1,67 m³ je Kammer; **A6 operativ: farbabhängig white 3,2 / green 2,1 / brown 1,1 m³**, V-3).

## 2. Datenmodell
- **Glas (Inhalt):** Farbe ∈ {braun, weiß, grün} (`brown`, `green`, `white`), Menge in % der Kammer.
- **Container (Puffer):** `Location_id` (449) mit Kammern je Farbe, Füllstand 0–100 %. Kammern: 441 IDs mit drei Farben, 7 mit zwei, 1 mit einer.
- **LKW (Consumer):** `besuch(datum, location_id)`. Zwei **verschiedene** Mengen, nicht verwechseln: er **leert alle** Kammern des Containers auf 0 (A1, Annahme), er **misst eine Teilmenge** der Kammern — 296 Besuche mit 1 Farbe, 1.111 mit 2, 3.061 mit 3 (`fakten.py` Abschnitt 4). Ein Besuch kann also alle Kammern leeren und trotzdem nur eine messen. Ob auch die **ungemessenen** Kammern geleert werden, entscheidet die CSV nicht: streng A1 (Leerung bei jedem Besuch) ergibt Median **9,7 Pp**, A4 (Leerung nur bei eigener Messung) **9,9 Pp** — innerhalb des Rauschens gleich (`fakten.py` Abschnitt 6). A1 bleibt deshalb gesetzte Annahme, nicht Befund.
- **Besuch** = (`Location_id`, `date`). Schlüssel. Der **Messwert ist der Füllstand vor der Leerung**; die Leerung selbst steht nie als Zeile in der CSV (A5, belegt in `fakten.py` Abschnitt 9).
- **Messung** = (`Location_id`, `material_type`, `date`) mit `fill_level_perc`. Schlüssel eindeutig.
- **Füllstand** = Prozent in 10er-Stufen, `overfull` = Text, Wert unbekannt (zensiert, mindestens 100).
- **Mengen:** Messungen (11.701), Besuche (4.468), Leerungen (= Besuche, Annahme A1), Überlauf-Messungen (1.192).
- Zeit hat nur Tagesauflösung. Rate = Prozent pro Tag.

## 3. Benannte Annahmen (neue nur mit Eintrag hier)
- A1: Jeder Besuch leert alle Farben der ID auf 0.
- A2: Füllrate je Container+Farbe ist zwischen Besuchen konstant (Startwert, wird geprüft).
- A3: `overfull` = Füllstand ≥ 100 %, genauer Wert unbekannt.
- A4: Jede Messung je (`Location_id`, `material_type`) ist zugleich eine Leerung dieses Containers auf 0; das tägliche Wachstum (`% pro Tag`) bemisst sich aus dem Abstand zur letzten Messung derselben (`Location_id`, `material_type`).
- A5: Gemessen wird **vor** der Leerung, geleert wird **nach** der Messung. Die CSV enthält keinen Stand nach dem Besuch, die Leerung ist also nicht direkt beobachtet, sondern nur über die Folgemessung prüfbar. Beleg (`fakten.py` Abschnitt 9, `n = 8.328` Paare mit numerischem Vorgängerstand): Start bei 0 ergibt **Median 9,5 Pp**, Wachstum ohne Leerung ab dem Vorgängerstand **24,4 Pp**; bei **40,7 %** der Paare liegt der nächste Stand niedriger als der vorherige. Die Leerung gewinnt. A5 sagt nur, **dass** geleert wird, nicht **welche** Kammern ein Besuch leert — dafür gilt A1.
- A6: Kammervolumen ist **farbabhängig**: white **3,2 m³**, green **2,1 m³**, brown **1,1 m³** je Farb-Behälter (recherchiert: IGF-Vorhaben 19596 N „intercon", TIB 1753684005 — Bedarfsvolumina proportional zum Sammelanteil der Farbfraktionen; kompakte 3-Kammer-Bauform dort als 3,2/1,89/0,68 m³ benannt). Eine Annahme für alle 449 Standorte; Quelle und Unsicherheit: `docs/externe_parameter.md` (V-3). Alle Volumina daraus sind „modelliert" und ersetzen nicht die Zielzahl (§5).
Jede Annahme, die ein Ergebnis verändert, wird im Ergebnis genannt.

## 4. Bilanztest = Gate
Ein Test (`tests/test_bilanz.py`) prüft die Realität, bevor etwas anderes gebaut wird:
1. Besuche = Leerungen im Modell (Anzahl identisch zur CSV: 4.468 Standort-Besuche, 11.701 Container-Messungen).
2. Rate × Abstand reproduziert den gemessenen Stand innerhalb eines **vorher festgelegten** Grenzwerts. Heute (`fakten.py` Abschnitt 6, $n = 9.206$ numerische Folgemessungen): Median-Fehler **9,9 Pp**, mittlerer Fehler **14,4 Pp**, P90-Fehler **36,3 Pp**, **53,2 %** innerhalb 10 Pp (inkl. 1.157 rechtszensierter `overfull`-Folgemessungen, $n = 10.363$: Median **8,9 Pp**, Mittel **13,9 Pp**, P90 **36,4 Pp**, **55,1 %** innerhalb 10 Pp). Festgelegter Grenzwert (Samuel): In-Sample **Median ≤ 10,0 Pp**, **P90 ≤ 37,0 Pp**, **Mittel ≤ 15,0 Pp**.
3. Das Modell erzeugt `overfull` ungefähr so oft wie die Daten (10,2 % gesamt / 11,2 % auf Folgemessungen; Modell bei nächster 10er-Stufe > 110 %: 12,2 % gesamt / 13,7 % auf Folgemessungen, Toleranz ± 4,0 Pp).
4. Backtest ohne Blick in die Zukunft: Training früher (≤ 2026-04-09), Test später (> 2026-04-09). Festgelegter Grenzwert (Samuel): Out-of-Sample **Median ≤ 16,0 Pp**, **P90 ≤ 50,0 Pp** (Ist numerisch, $n = 5.239$: Median **15,1 Pp**, P90 **48,1 Pp**, Mittel **20,4 Pp**; inkl. zensiert, $n = 5.948$: Median **14,3 Pp**, P90 **48,7 Pp**, Mittel **19,8 Pp**).

## 5. Die eine Zielzahl
**Eingesparte Leerungen in % gegenüber dem Ist-Plan, bei höchstens gleicher Überlaufquote.**
Ein Plan mit mehr Besuchen oder mehr Überlauf als der Ist-Plan ist kein Erfolg, egal wie schön.
Der frühere Ansatz hat Überlauf wegoptimiert und dafür deutlich mehr gefahren (Größenordnung nicht aus der CSV belegt). Das ist die falsche Richtung.
Die operative Zielzahl ist damit vollständig aus internen Daten berechenbar. Zusätzliche absolute Mengenziele (z. B. eingespartes Glasvolumen in m³ oder Tonnen) sind **sekundäre, externe Ergebnisse**: Sie setzen recherchierte, dokumentierte Parameter mit Unsicherheit voraus und ersetzen die primäre Zielzahl nicht.

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
