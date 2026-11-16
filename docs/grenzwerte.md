# Grenzwerte (Bilanz-Gate) — Herkunft, Baseline, Kalibrierung

Stand: 2026-11-16. Regel ab jetzt: **Grenzwerte werden VOR dem Lauf festgelegt und nie
nach einem Ergebnis gelockert.** Jede Änderung braucht eine Begründung, die unabhängig
von den Modell-Ergebnissen ist (Messauflösung, Baseline, Owner-Entscheid mit Datum).

## 1. Archäologie (git log/diff, 2026-11-16)

- Die heutigen Grenzwerte wurden in **einem einzigen Commit** eingeführt
  (`d17f7cb` „feat(sim): publish glass container simulation and kino") — **zusammen**
  mit den Tests und den Ist-Werten in `AGENTS.md` §4. Vorher (bis `f2104ff`) stand
  dort nur: „Grenzwert legt Samuel fest, nicht der Agent" — **ohne Zahl**.
- Jeder Grenzwert sitzt knapp über dem gemessenen Ist desselben Commits:
  Median 9,9 → 10,0 · P90 36,3 → 37,0 · MAE 14,4 → 15,0 · OOS-Median 15,1 → 16,0 ·
  OOS-P90 48,1 → 50,0. Das ist **post-hoc**: aus den Ergebnissen abgeleitet, nicht
  unabhängig begründet.
- Der ursprüngliche Grenzwert **„MAE ≤ 12 Pp" ist in der Git-Historie dieses Repos
  nicht auffindbar** (nur zwei Commits berühren `AGENTS.md`). Fakt notiert; der Wert
  kommt lt. Samuel aus der Zeit vor dem Restart.
- **Entscheid (Samuel, 2026-11-16):** In-Sample Mittel (MAE) ≤ 15,0 → **≤ 12,0 Pp**
  zurückgesetzt. Übrige Grenzwerte bleiben (Owner-Entscheid; die post-hoc-Herkunft
  von OOS ≤ 16,0/50,0 ist hiermit dokumentiert, nicht neu gerechtfertigt).
- **Korrektur (2026-11-16):** Für die 12,0-Diskussion wurde zunächst eine
  Klassenschranke von **12,8 Pp** gemessen — diese Zahl war **container-ungewichtet**
  (jeder Container gleich viel) und für das Gate, das **zeilengewichtet** auswertet,
  falsch. In Gate-Semantik liegt die Klassenschranke bei **13,6 Pp**
  (`fakten.py` Abschnitt 12.5 F). Die vorläufige Empfehlung „≤ 13,0" wurde
  zurückgezogen (13,0 ist in der Klasse unerreichbar).
- **Entscheid (Samuel, 2026-11-16, korrigiert):** Grenzwert MAE **≤ 14,0 Pp**,
  begründet mit der zeilengewichteten Klassenschranke 13,6 Pp als unabhängigem Anker
  (Eigenschaft der Daten + Modellklasse, nicht eines getunten Modells), **plus
  Schätzer-Wechsel** von „Median der Quotienten" auf **MAE-Fit je Container**
  (`rate_fit`, `src/modell.py`, Abschnitt 12.5 F). Der Schätzer erreicht die
  Klassenschranke exakt (Ist MAE 13,6). Siehe auch §2 (Klassenschranke) und §3.

## 2. Unabhängige Anker

**Messauflösung (Floor):** Die Skala ist in 10er-Stufen aufgeteilt. Reines
Rundungsrauschen eines perfekten Vorhersagens ergibt MAE ≈ **2,5 Pp**
(Median ≈ 2,5, P90 ≈ 4,5). Kein Grenzwert kann sinnvoll darunter liegen; MAE ≤ 14,0
liegt darüber. Der frühere Grenzwert 12,0 lag über dem Rundungs-Floor, aber
**unter der Klassenschranke** (13,6 Pp, siehe unten) — er war damit nicht durch die
Messauflösung blockiert, sondern durch die Modellklasse.

**Klassenschranke (Anker für MAE ≤ 14,0, `fakten.py` Abschnitt 12.5 F):** Innerhalb
der Modellklasse „eine konstante Rate je Container+Farbe" ist der bestmögliche MAE
eine Eigenschaft der Daten: Selbst die Rate, die pro Container den MAE minimal macht
(clipping-bewusst, in-sample geschummelt — untere Schranke der Klasse), liegt bei
**13,6 Pp** (zeilengewichtet, n = 9.206). Der Grenzwert MAE ≤ 14,0 Pp sitzt knapp
über dieser Schranke. Das frühere MAE-Ziel 12,0 lag **unterhalb** der Schranke und
war in dieser Klasse prinzipiell unerreichbar — die „unerreichbar"-Messung
(`fakten.py` Abschnitt 12.3, globale Skala k* = 1,02 → 14,4) ist die unabhängige
Begründung für die Neu-Festlegung, nicht das Ergebnis des neuen Schätzers.

**Naive Baselines** (gleiche Grundmenge wie `fehler_numerisch`: 9.206 numerische
Folgemessungen; Ausgabe: `data/derived/baseline_grenzwerte.csv`, berechnet aus
`lade_messungen()`, keine Modellraten):

| Modell | Median Pp | P90 Pp | MAE Pp | n |
|---|---|---|---|---|
| B1 globaler Mittelwert (61,0 %) | 29,0 | 41,0 | 25,3 | 9.206 |
| B2 Mittelwert je Farbe | 17,5 | 35,9 | 20,8 | 9.206 |
| B3 Rate je Farbe, Median, ohne Ort (brown 0,97 / green 2,38 / white 3,08 %/Tag) | 20,6 | 55,4 | 25,6 | 9.206 |
| **Modell (Rate je Ort+Farbe, `rate_fit`)** | **8,7** | **36,4** | **13,6** | 9.206 |

Bewertung: Das Modell schlägt alle drei Baseline-Modelle klar bei **Median** (−50 %
vs. der besten Baseline B2) und **MAE** (−35 % vs. B2). Bei **P90** liegt es knapp
hinter B2 (36,4 vs. 35,9 Pp, +0,5 Pp = Rauschen an der gleichen Stelle). MAE ≤ 14,0
liegt deutlich unter der besten Baseline (20,8) — das „klar schlagen"-Kriterium ist
damit messbar verankert.

## 3. Aktuelle Grenzwerte des Bilanz-Gates (AGENTS.md §4, modell.py)

Ist-Stand 2026-11-16 nach Schätzer-Wechsel (`rate_fit` = MAE-Fit je Container,
Abschnitt 12.5 F):

| Prüfung | Grenzwert | Ist (2026-11-16) | Status |
|---|---|---|---|
| In-Sample Median | ≤ 10,0 Pp | 8,7 | ✅ |
| In-Sample P90 | ≤ 37,0 Pp | 36,4 | ✅ |
| In-Sample MAE | ≤ **14,0 Pp** | 13,6 (= Klassenschranke) | ✅ |
| Überlauf-Quote (Folgemessungen) | ± 4,0 Pp | Daten 11,2 % / Modell 19,2 % | ❌ **ROT — parkiert** |
| Backtest OOS Median | ≤ 16,0 Pp | 15,2 | ✅ |
| Backtest OOS P90 | ≤ 50,0 Pp | 49,3 | ✅ |

Stand des Gates: Der MAE ist grün (der neue Schätzer erreicht die Klassenschranke
13,6 exakt), Median/P90/OOS bleiben grün. **Rot bleibt die Überlauf-Quote** — und
sie hat sich durch den Schätzer-Wechsel verschärft (Modell 13,7 % → 19,2 %;
Kalibrierung §4: 18,3 % → 24,0 %). Das Gate ist damit weiterhin rot; die
Fächeransicht bleibt blockiert (AGENTS.md §6).

**Gemessene Ursache (`fakten.py` Abschnitte 13–13.2, reine Messung):** 19,0 % aller
numerischen Zeilen stehen exakt auf 100 (Spike; die Nachbarstufe 90 nur 9,4 %).
In der MAE-Verlustfunktion ist Über-Vorhersage an solchen Zeilen gratis
(`|clip(r·dt, 0, 100) − p| = 0` für jede r ≥ 100/dt) — der Fit bläht genau die
Überlauf-Region auf (Raten-Inflation konzentriert auf Container mit vielen
p ≥ 90-Zeilen: Median 1,14×; Container ohne solche: 0,94×). 55,3 % der
p == 100-Zeilen sind unter A1/A2 „zu voll".

**Parkiert (Samuel, 2026-11-16):** Hypothese **A3b** — die exakte 100-Lesung ist
verdeckte Rechtszensierung (Leser schreibt `100`, wenn die Kammer voll ist, wahrer
Stand ≥ 100 %, analog A3 für `overfull`). Das wäre eine Wurzel für beide
beobachteten Probleme (Raten-Inflation des MAE-Fit **und** den schon mit dem alten
Median-Schätzer vorhandenen Überlauf-Überschuss). Aktivierung nur durch Samuel;
vor Code steht die reine Messung des Kandidaten (p == 100 wie zensiert behandeln,
MAE + Überlaufquote für beide Schätzer). Kein Grenzwert wird verändert.

## 4. Kalibrierungs-Grenzwerte (`tests/test_kalibrierung.py`)

Vor dem ersten Lauf festgelegt (2026-11-16, vor Ausführung). Grundgesamtheit:
alle **Folgemessungen** der CSV (`abstand > 0`, n = 10.363 inkl. zensiert;
numerisch n = 9.206) — Simulation und Echt werden identisch beobachtet.

Beobachtungsmodell (Annahmen, vorab fixiert):
- **OBS-1:** kontinuierlicher simulierter Stand → 10er-Stufe per Runden auf die
  nächste Stufe (`floor(x/10 + 0.5) * 10`). Die echte Ablese-Regel ist unbekannt;
  nächstgelegene Stufe ist die mildeste Annahme.
- **OBS-2:** Stand > 100 % → Text `overfull` (rechtszensiert, A3); Stand = 100 % → 100.
- **OBS-3:** gemessen wird nur bei echten Besuchen, echte Besuchsdaten, fehlende
  Farben wie in der CSV (simuliert werden genau die existierenden Mess-Zeilen).
- **OBS-4:** generative Rate = `rate_fit` (MAE-Fit je Container, `src/modell.py`,
  Entscheid Samuel 2026-11-16) aus `schaetze_fuellraten()`; Zeilen ohne Rate und
  erste Messungen (kein Vorgänger) fliegen heraus (Anzahl berichtet).

| Prüfung | Grenzwert | Unabhängige Begründung |
|---|---|---|
| Overfull-Quote gesamt (Folge) | \|sim−echt\| ≤ 4,0 Pp | Bestehende ± 4,0-Pp-Toleranz aus AGENTS.md §4.3 |
| Overfull-Quote je Farbe (3×) | \|sim−echt\| ≤ 4,0 Pp | dito |
| Quantile P10/P50/P90 numerisch (3×) | \|sim−echt\| ≤ 10,0 Pp | eine Skalenstufe (10er-Auflösung) |
| Median je Abstands-Bucket ≤7 / 8–14 / 15–30 / >30 Tage (4×) | \|sim−echt\| ≤ 10,0 Pp | eine Skalenstufe |

Die KS-Statistik wird als Information mitberichtet (ohne Grenzwert). Läuft die
Kalibrierung rot, bleibt sie rot — **nichts tunen, nur berichten**.

### Erstlauf (2026-11-16, Median der Quotienten) — Quelle: `data/derived/kalibrierung.json`

n = 10.363 Folgemessungen (numerisch: 8.008, weil simulierte `overfull`-Zeilen auf
beiden Seiten zensiert sind; 0 Zeilen ohne Rate). KS-Statistik: **0,094**.

| Prüfung | Echt | Simuliert | Diff | Grenzwert | Status |
|---|---|---|---|---|---|
| Overfull-Quote gesamt | 11,2 % | 18,3 % | +7,1 Pp | ≤ 4,0 | ❌ |
| Overfull-Quote white | 17,8 % | 28,8 % | +11,1 Pp | ≤ 4,0 | ❌ |
| Overfull-Quote green | 9,4 % | 16,4 % | +7,0 Pp | ≤ 4,0 | ❌ |
| Overfull-Quote brown | 3,7 % | 5,2 % | +1,5 Pp | ≤ 4,0 | ✅ |
| P10 numerisch | 20 % | 20 % | 0,0 Pp | ≤ 10,0 | ✅ |
| P50 numerisch | 60 % | 60 % | 0,0 Pp | ≤ 10,0 | ✅ |
| P90 numerisch | 100 % | 90 % | −10,0 Pp | ≤ 10,0 | ✅ (grenzwertig) |
| Median Bucket ≤7 Tage | 40 % | 30 % | −10,0 Pp | ≤ 10,0 | ✅ (grenzwertig, n=291) |
| Median Bucket 8–14 Tage | 50 % | 50 % | 0,0 Pp | ≤ 10,0 | ✅ |
| Median Bucket 15–30 Tage | 60 % | 60 % | 0,0 Pp | ≤ 10,0 | ✅ |
| Median Bucket >30 Tage | 70 % | 60 % | −10,0 Pp | ≤ 10,0 | ✅ (grenzwertig) |

Ergebnis: **3 von 11 rot, 3 weitere grenzwertig grün** (genau am Limit). Die roten
Prüfungen betreffen alle die Überlauf-Quote: Die Simulation erzeugt deutlich mehr
Überlauf als die echten Daten.

### Nach dem Schätzer-Wechsel (2026-11-16, `rate_fit` = MAE-Fit) — Quelle: `data/derived/kalibrierung.json`

n = 10.363 Folgemessungen (numerisch: 7.481, weil mehr simulierte `overfull`-Zeilen
auf beiden Seiten zensiert sind; 0 Zeilen ohne Rate). KS-Statistik: **0,068**.

| Prüfung | Echt | Simuliert | Diff | Grenzwert | Status |
|---|---|---|---|---|---|
| Overfull-Quote gesamt | 11,2 % | 24,0 % | +12,9 Pp | ≤ 4,0 | ❌ |
| Overfull-Quote white | 17,8 % | 38,0 % | +20,2 Pp | ≤ 4,0 | ❌ |
| Overfull-Quote green | 9,4 % | 22,0 % | +12,6 Pp | ≤ 4,0 | ❌ |
| Overfull-Quote brown | 3,7 % | 5,9 % | +2,2 Pp | ≤ 4,0 | ✅ |
| P10 numerisch | 20 % | 20 % | 0,0 Pp | ≤ 10,0 | ✅ |
| P50 numerisch | 60 % | 50 % | −10,0 Pp | ≤ 10,0 | ✅ (grenzwertig) |
| P90 numerisch | 90 % | 90 % | 0,0 Pp | ≤ 10,0 | ✅ |
| Median Bucket ≤7 Tage | 40 % | 30 % | −10,0 Pp | ≤ 10,0 | ✅ (grenzwertig, n=291) |
| Median Bucket 8–14 Tage | 50 % | 50 % | 0,0 Pp | ≤ 10,0 | ✅ |
| Median Bucket 15–30 Tage | 60 % | 60 % | 0,0 Pp | ≤ 10,0 | ✅ |
| Median Bucket >30 Tage | 70 % | 60 % | −10,0 Pp | ≤ 10,0 | ✅ (grenzwertig) |

Ergebnis: weiterhin **3 von 11 rot** (alle Überlauf-Quote), die Differenzen sind
größer als im Erstlauf (+12,9/+20,2/+12,6 statt +7,1/+11,1/+7,0 Pp). Zusätzlich ist
nun auch die Bilanz-Überlaufquote (`tests/test_bilanz.py` Test 3) rot: Modell
19,2 % vs. Daten 11,2 % auf Folgemessungen. Die parkierte Hypothese A3b (§3) ist
der Kandidat, um beide Beobachtungen zu erklären; es wird nichts getunt.
