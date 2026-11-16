# Externe Parameter

Getrennt von den internen Fakten (`scripts/fakten.py`). Jeder Parameter: Wert, Einheit,
Geltungsbereich, Quelle, Abrufdatum, Unsicherheit. Recherche-Datum: **2026-11-16**.

## V-1 Kammervolumen (Glas-Depotcontainer)

- **Wert (Bandbreite):** 0,53 m³ (klein) / **1,07 m³ (Standard)** / 1,67 m³ (groß) je Kammer
- **Einheit:** m³ pro Farb-Kammer
- **Geltungsbereich:** Glas-Depotcontainer nach DIN EN 13071, 3-Kammer-Ausführung. Unsere Daten
  haben 441 von 449 Standorten mit 3 Kammern (`fakten.py` Abschnitt 3) — genau der Standard-Dreikammer-Container.
- **Quellen:**
  - SSI Schäfer, Depotcontainer-Datenblatt (PDF, ssi-schaefer.com): Nenninhalte **1,6 / 3,2 / 5,0 m³**,
    mit Trennwänden in 2–3 Kammern teilbar, „alle Werte sind Circa-Maße in Anlehnung an DIN 13071“.
    3 Kammern aus 3,2 m³ → ≈ 1,07 m³ je Kammer (Trennwände reduzieren leicht).
  - Krauß Umwelttechnik, depotcontainer (krauss-umwelttechnik.de): Größen **1,1–5,0 m³**, 3-Kammer-Ausführung.
  - Blauer Engel DE-UZ 21 (blauer-engel.de), gelistete Altglas-Container: Nenninhalte 2,5 / 3,0 / 3,2 / 3,5 m³ —
    bestätigt die Größenordnung des Standards um 3,0–3,5 m³ gesamt.
  - GWWN Altglascontainer-Katalog (gwwn.at): 750 L / 1.500 L (je Kammer 750 L) / 3.000 L
    (je Kammer 1.500 L) — deckt das Band unten ab (Österreich, andere Baureihe).
- **Bandbreite (Sensitivity):**
  - klein: 1,6 m³ Container, 3 Kammern → ≈ 0,53 m³ je Kammer
  - Standard: 3,2 m³ Container, 3 Kammern → ≈ 1,07 m³ je Kammer (**Referenzwert**)
  - groß: 5,0 m³ Container, 3 Kammern → ≈ 1,67 m³ je Kammer
- **Unsicherheit:** hoch. Containermodell bei PreZero nicht belegt (Daten anonymisiert); Nenninhalte sind
  Circa-Maße; tatsächlich nutzbares Kammervolumen liegt wegen Trennwänden unter dem Quotienten. Deshalb
  **nur als Bandbreite ausweisen**, nie als exakte CSV-Wahrheit (AGENTS.md §1).

## V-3 Kammervolumen farbabhängig (Annahme A6)

- **Werte (Referenz, Annahme A6):** white **3,2 m³** / green **2,1 m³** / brown **1,1 m³** je Farb-Behälter
- **Alternative (kompakte 3-Kammer-Bauform):** white 3,2 / green 1,89 / brown 0,68 m³
- **Einheit:** m³ Innenvolumen je Farb-Behälter
- **Geltungsbereich:** bedarfsorientierte Behältergrößen proportional zum Sammelanteil der
  Farbfraktionen in Deutschland (Grünglas ≈ 2/3 von Buntglas-Anteil, Braunglas ≈ 1/3), abgeleitet
  vom Standarddepotcontainervolumen 3,2 m³. Passt zum Überlauf-Muster in den Daten
  (white 731 / green 357 / brown 104 überfüllte Messungen, `fakten.py` Abschnitt 3).
- **Quelle:** Schlussbericht IGF-Vorhaben 19596 N „intercon" (PDF, edocs.tib.eu/files/e01fn21/1753684005.pdf):
  „das in der Praxis zur Weißglassammlung am häufigsten eingesetzte und bewährte
  Depotcontainerinnenvolumen von 3,2 m³", Standarddepotcontainervolumen 3,2 m³;
  daraus erforderliche Volumina Weißglas 3,2 / Grünglas 2,1 / Braunglas 1,1 m³;
  im Konstruktionskapitel der 3-Kammer-Variante Weißglasbehälter ca. 3,2 m³,
  Grünglaskammer ca. 1,89 m³, Braunglaskammer ca. 0,68 m³. Abrufdatum: **2026-11-16**.
- **Unsicherheit:** mittel. Werte stammen aus einem Forschungsbericht, nicht aus einer Norm oder
  PreZero-Spezifikation; die Daten sind anonymisiert (Containermodelle nicht belegt), eine Annahme
  für alle 449 Standorte. Deshalb bleibt alles „modelliert" (A6), nie CSV-Wahrheit.

## V-2 overfull (rechtszensiert)

- **Wert:** ≥ 100 % der Kammer, genauer Wert unbekannt (A3).
- **Konsequenz für Volumen:** Volume hinter `overfull` ist ein **Minimum** (≥ 1,0 × Kammervolumen).
  Wird im Ergebnis immer als Untergrenze ausgewiesen, nie als exakter Wert.
