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

## V-5 LKW-Objekte (Platzhalter — ohne Wirkung auf die Simulation)

**Status: Platzhalter.** Diese Werte sind **recherchiert** (Herstellerangaben), **nicht gemessen**
und **nicht modelliert** — sie gehen **nicht** in die Simulation ein. Sie dienen ausschließlich der
Beschriftung im Drehbuch und den Vorschau-Bildern (`scripts/bilder_lkw.py`).
Recherche-Datum: **2026-11-16**. Upstream-Evidenz: `docs/UPSTREAM_SEARCH.md` (Abschnitt C).

| Objekt | Hersteller | Ladevolumen | Orte je Tour (bei 4,35 m³ je Stopp) | Quelle |
|---|---|---|---|---|
| Glas-Sammelfahrzeug GC 23 | Stummer | 23 m³ | 5,3 | Fact Sheet PDF (C1) |
| Hecklader MEDIUM X4H | Zoeller | 14–29 m³ | 6,7 (bei 29 m³) | Datenblatt PDF (C2) |
| Hakenlift Eurolift HL | Stummer | 18–31 m³ | 7,1 (bei 31 m³) | Produktseite (C3) |
| Presse 20 m³ | REMONDIS | 20 m³ | 4,6 | Sammelsysteme PDF (C5) |
| Abrollkipper ARKM 36 | REMONDIS | 36 m³ | 8,3 | Sammelsysteme PDF (C5) |
| **Grenzfall: 1 voller PreZero-Standort** | A6/V-3 | **6,4 m³** | 1,5 | CSV + A6 |

- **Geltungsbereich:** Ladevolumen des Aufbaus (Nutzvolumen), nicht Nutzlast in kg. Bei
  Presse- und Abrollkipper-Systemen ist der Container selbst das Ladeobjekt.
- **Unsicherheit:** **hoch.** Herstellerangaben für Serienmodelle, nicht PreZero-Spezifikation;
  die Container-Zuordnung zu unseren 449 Standorten ist unbekannt (Daten anonymisiert). Die
  Spalte „Orte je Tour" ist eine **Rechnung aus der beobachteten Median-Ladung** (4,35 m³,
  obere Schranke aus 4.468 Besuchen) — sie unterstellt, dass ein LKW mehrere Standorte je Tour
  bedient. **Das zeigen die Daten nicht** (siehe unten).

### Warum Platzhalter und kein Modellparameter

Aus `data/raw/glass_fill_levels_anonymized_f.csv` (4.468 Besuche, A6/V-3):

| Größe | Wert | Art |
|---|---|---|
| Ladung je Besuch, obere Schranke | Median **4,35 m³** · P90 5,86 · max **6,40** | gemessen + A6 |
| Anteil Besuche mit Ladung > 6,4 m³ | **0,0 %** | gemessen + A6 |
| Zufluss > Entnahme je Kammer | **47,4 %** der Fälle | gemessen + A6 |

1. Der beobachtete Rhythmus ist **bilanziert** — Zufluss und Entnahme gleichen sich.
2. **Kein beobachteter Besuch** überschreitet 6,4 m³ (= ein voller 3-Kammer-Standort).
3. Kapazität **< 6,4 m³** im Modell: Restmengen bleiben stehen, das System flutet
   (Überlauf **4,91 % → ~96 %**, nachgerechnet). Der Ist-Lauf wäre zerstört.
4. Kapazität **≥ 6,4 m³** im Modell: **kein Unterschied** — ein Mehrfach-Stopp je Tour ist in den
   Daten nicht belegt (ein Besuch = ein Ort).

**Also:** Die Kapazität als Modellparameter entweder zerstört den Ist-Lauf oder tut nichts.
Ein Platzhalter ist die einzig wahre Abbildung: die Zahl ist recherchierbar, ihre **Wirkung auf
den Takt** ist es nicht. Die Marktfahrzeuge fahren 3–8 Orte je Tour, die Daten zeigen **einen
Besuch je Ort** — der Unterschied ist nicht die Kapazität, sondern der Takt.

## V-4 Festgehaltenes Volumen-Ergebnis (Stand 2026-11-16)

Operative Setzung: **A6 (farbabhängig)** — siehe V-3. Alle Volumina „modelliert", Füllstände „gemessen"
(`scripts/volumen_sensitivity.py`, CSV 11.701 Messungen, 12 Monate).

| Farbe | Behälter (A6) | Volumen 12 Monate | A6-kompakt |
|---|---|---|---|
| white | 3,2 m³ | 11.424 m³ | 11.424 m³ |
| green | 2,1 m³ | 5.884 m³ | 5.296 m³ |
| brown | 1,1 m³ | 1.351 m³ | 835 m³ |
| **Σ** | | **18.659 m³** | **17.555 m³** |

- Vergleich gleichmäßige Kammer (V-1): 4.028 – 8.132 – 12.692 m³.
- Ø Volumen je Besuch (nur gemessene Kammern, Untergrenze): Median 4,35 m³, Mittel 4,18 m³, P90 5,86 m³.
- Volumen je Standort über den Zeitraum: Median 36,9 m³ (P10 14,0 / P90 74,6 m³) — entspricht ~6 Füllzyklen
  pro Jahr bei 6,4 m³ Aufstellung je Standort.
- Mindestvolumen hinter `overfull`: ≥ 3.203 m³ (white 2.339 / green 750 / brown 114 m³), exakt unbekannt (A3).
- **Befund:** Die absolute Volumenzahl hängt fast vollständig an der Containerannahme, nicht an den Daten.
  Daten halten solide (Füllstände, Raten, Überlaufmuster); das Muster passt zu A6 (white überläuft am häufigsten).
  Die Zielzahl („eingesparte Leerungen in %", AGENTS.md §5) bleibt von A6 unberührt.

### Parkierte Optionen (festgehalten, NICHT operativ — Stand 2026-11-16)

Möglichkeiten, die A6 später eröffnen kann. Keine davon ist aktiv; die Zielzahl bleibt „eingesparte Leerungen in %“ (§5).

- **Opt-1 Volumen-/Auslastungssteuerung:** Optimierung oder Schwellenwerte **farbabhängig** in %
  setzen (Behältergrößen differieren: 50 % white ≈ 1,6 m³, 50 % brown ≈ 0,55 m³). Bliebe intern
  (%) umsetzbar, benötigt aber A6 als Entscheidungsgröße statt Sekundärmetrik.
- **Opt-2 Auslastung als Nebenbedingung oder Sekundärziel:** z. B. „m³ je eingesparter Fahrt“
  oder Auslastungs-Minimum je Farbe neben der Zielzahl.
- **Bedingung für Aktivierung:** nur wenn Samuel die Zielzahl ändert/erweitert **und** die
  Containerannahme belastbarer ist (z. B. echte PreZero-Behälterspezifikation statt Forschungsbericht).
  Solange das fehlt, bleibt Volumen Sensitivity-Bandbreite (§1), keine Optimierungsgröße.

## V-2 overfull (rechtszensiert)

- **Wert:** ≥ 100 % der Kammer, genauer Wert unbekannt (A3).
- **Konsequenz für Volumen:** Volume hinter `overfull` ist ein **Minimum** (≥ 1,0 × Kammervolumen).
  Wird im Ergebnis immer als Untergrenze ausgewiesen, nie als exakter Wert.
