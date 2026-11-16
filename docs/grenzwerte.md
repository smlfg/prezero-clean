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

## 2. Unabhängige Anker

**Messauflösung (Floor):** Die Skala ist in 10er-Stufen aufgeteilt. Reines
Rundungsrauschen eines perfekten Vorhersagens ergibt MAE ≈ **2,5 Pp**
(Median ≈ 2,5, P90 ≈ 4,5). Kein Grenzwert kann sinnvoll darunter liegen; MAE ≤ 12,0
liegt darüber und ist damit prinzipiell erreichbar.

**Naive Baselines** (gleiche Grundmenge wie `fehler_numerisch`: 9.206 numerische
Folgemessungen; Ausgabe: `data/derived/baseline_grenzwerte.csv`, berechnet aus
`lade_messungen()`, keine Modellraten):

| Modell | Median Pp | P90 Pp | MAE Pp | n |
|---|---|---|---|---|
| B1 globaler Mittelwert (61,0 %) | 29,0 | 41,0 | 25,3 | 9.206 |
| B2 Mittelwert je Farbe | 17,5 | 35,9 | 20,8 | 9.206 |
| B3 Rate je Farbe, Median, ohne Ort (brown 0,97 / green 2,38 / white 3,08 %/Tag) | 20,6 | 55,4 | 25,6 | 9.206 |
| **Modell (Rate je Ort+Farbe)** | **9,9** | **36,3** | **14,4** | 9.206 |

Bewertung: Das Modell schlägt alle drei Baseline-Modelle klar bei **Median** (−43 %
vs. der besten Baseline B2) und **MAE** (−31 % vs. B2). Bei **P90** liegt es knapp
hinter B2 (36,3 vs. 35,9 Pp, −0,4 Pp = Rauschen an der gleichen Stelle). MAE ≤ 12,0
liegt deutlich unter der besten Baseline (20,8) — das „klar schlagen"-Kriterium ist
damit messbar verankert.

## 3. Aktuelle Grenzwerte des Bilanz-Gates (AGENTS.md §4, modell.py)

| Prüfung | Grenzwert | Ist (2026-11-16) | Status |
|---|---|---|---|
| In-Sample Median | ≤ 10,0 Pp | 9,9 | ✅ |
| In-Sample P90 | ≤ 37,0 Pp | 36,3 | ✅ |
| In-Sample MAE | ≤ **12,0 Pp** | 14,4 | ❌ **ROT seit Reset — bleibt rot** |
| Überlauf-Quote (Folgemessungen) | ± 4,0 Pp | Daten 11,2 % / Modell 13,7 % | ✅ |
| Backtest OOS Median | ≤ 16,0 Pp | 15,1 | ✅ |
| Backtest OOS P90 | ≤ 50,0 Pp | 48,1 | ✅ |

Der In-Sample-MAE überschreitet den zurückgesetzten Grenzwert um 2,4 Pp. Das Gate
bleibt rot, bis das Modell besser ist — **kein Tunen an den Grenzwerten**.

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
- **OBS-4:** generative Rate = `rate_med` je (`Location_id`, `material_type`) aus
  `schaetze_fuellraten()`; Zeilen ohne Rate und erste Messungen (kein Vorgänger)
  fliegen heraus (Anzahl berichtet).

| Prüfung | Grenzwert | Unabhängige Begründung |
|---|---|---|
| Overfull-Quote gesamt (Folge) | \|sim−echt\| ≤ 4,0 Pp | Bestehende ± 4,0-Pp-Toleranz aus AGENTS.md §4.3 |
| Overfull-Quote je Farbe (3×) | \|sim−echt\| ≤ 4,0 Pp | dito |
| Quantile P10/P50/P90 numerisch (3×) | \|sim−echt\| ≤ 10,0 Pp | eine Skalenstufe (10er-Auflösung) |
| Median je Abstands-Bucket ≤7 / 8–14 / 15–30 / >30 Tage (4×) | \|sim−echt\| ≤ 10,0 Pp | eine Skalenstufe |

Die KS-Statistik wird als Information mitberichtet (ohne Grenzwert). Läuft die
Kalibrierung rot, bleibt sie rot — **nichts tunen, nur berichten**.

### Erstlauf (2026-11-16) — Quelle: `tests/test_kalibrierung.py` → `data/derived/kalibrierung.json`

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
