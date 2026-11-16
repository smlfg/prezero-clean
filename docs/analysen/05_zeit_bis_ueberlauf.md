# 05 – Zeit bis zum erwarteten Überlauf

> 462 von 1.338 Zeitreihen (34,5%) stehen bei der letzten Messung bereits auf ≥80%,
> die mediane Reihe erreicht 80% in 32 Tagen und 100% in 58 Tagen, und 196 weitere
> Reihen kippen innerhalb von 30 Tagen über die 80%-Schwelle.

## Frage

Wie viele Tage dauert es ab der letzten Messung einer Zeitreihe, bis der Container
80% bzw. 100% Füllstand erreicht? Wie verteilen sich die Reihen auf Dringlichkeits-
klassen, und wie stark verschiebt sich das Bild bei optimistischer bzw. pessimistischer
Füllrate?

## Vorgehen

- Datengrundlage: `../glass_fill_levels_anonymized_f.csv`, 11.701 Messungen, 1.338
  Zeitreihen (`Location_id` × `material_type`), 229 Messtage; `overfull` als 110 kodiert
  (tatsächliche Höhe unbekannt).
- **Füllrate** je Zeitreihe: `rate = Δpp / ΔTage` über aufeinanderfolgende Messungen;
  negative und Nullsprünge verworfen. Kennzahl = Median der positiven Raten (plus P25/P75).
- **Fallback** für Reihen ohne positiven Übergang (103 Reihen, davon 34 mit nur einer
  Messung): Material-Median der Reihen-Mediane (braun 0,51 · grün 0,77 · weiß 0,71 pp/Tag).
- `Tage_bis_X = max(0, (X − letzter Stand) / Rate)`. Steht die Reihe schon ≥ X, ist das
  Ergebnis 0 → Klasse „bereits kritisch“. Alle 1.338 Reihen sind rechenbar, „nicht
  schätzbar“ bleibt daher leer.

## Ergebnisse

| Kennzahl | Wert |
|---|---|
| Übergänge gesamt | 10.363 — positiv 4.341 (41,9%) · negativ 4.266 (41,1%) · unverändert 1.756 (16,9%) |
| Rate aller positiven Übergänge | Median 0,74 pp/Tag · P25 0,38 · P75 1,43 · Max 25,0 |
| Reihen-Median (n=1.235) | Median 0,68 pp/Tag · P25 0,41 · P75 1,01 · Max 13,3 |
| Messabstand | 28 Tage über alle Übergänge, 35 Tage je Zeitreihe |

### Dringlichkeitsklassen (Rate = Reihen-Median)

| Klasse | bis 80% | bis 100% | bis 80% (P75-Rate) | bis 80% (P25-Rate) |
|---|---|---|---|---|
| bereits kritisch (≤0 Tage) | **462** | **280** | 462 | 462 |
| 0–7 Tage | 12 | 9 | 30 | 7 |
| 8–14 Tage | 52 | 60 | 87 | 23 |
| 15–30 Tage | 132 | 114 | 179 | 100 |
| >30 Tage | 680 | 875 | 580 | 746 |
| nicht schätzbar | 0 | 0 | 0 | 0 |

Median über alle Reihen: **32,0 Tage bis 80%**, **58,1 Tage bis 100%**. Nur 196 Reihen
(14,7%) liegen im Fenster „0–30 Tage, noch nicht kritisch“ — das ist die Arbeitsliste.

### Nach Material

| Material | Reihen | davon ≥80% | Median Tage→80% | Median Tage→100% | 0–30 Tage, nicht kritisch |
|---|---|---|---|---|---|
| braun | 442 | 42 | 97,7 | 140,6 | 31 |
| grün | 448 | 155 | 26,0 | 47,9 | 87 |
| weiß | 448 | 265 | 0,0 | 22,1 | 78 |

### Die 25 dringendsten, noch nicht kritischen Reihen

Sortiert nach Tagen bis 80% (Median-Rate); 13 grün, 10 weiß, 2 braun, mediane letzte
Messung 2026-09-11. „Spanne“ = Tage bei 75.-Perzentil-Rate bis Tage bei 25.-Perzentil-Rate
der Reihe. Stand in %, Datum = letzte Messung.

| # | Location_id | Mat | Letzte Messung | Stand | Rate Med | Tage→80% | Spanne | Tage→100% |
|---|---|---|---|---|---|---|---|---|
| 1 | `b3a9f61a…` | green | 2026-08-24 | 50 | 13,31 | **2,3** | 2–4 | 3,8 |
| 2 | `0c6aa0da…` | green | 2026-08-19 | 70 | 3,04 | **3,3** | 3–3 | 9,9 |
| 3 | `9714654e…` | brown | 2026-09-29 | 70 | 2,93 | **3,4** | 2–4 | 10,2 |
| 4 | `0786a63c…` | white | 2026-09-17 | 70 | 2,33 | **4,3** | 3–6 | 12,9 |
| 5 | `50358b29…` | green | 2026-09-11 | 70 | 2,16 | **4,6** | 4–5 | 13,9 |
| 6 | `fdccb1ff…` | green | 2026-09-09 | 70 | 1,74 | **5,7** | 4–7 | 17,2 |
| 7 | `dcc3bbe3…` | white | 2026-09-17 | 70 | 1,69 | **5,9** | 4–11 | 17,7 |
| 8 | `8d75ce98…` | green | 2026-09-09 | 70 | 1,52 | **6,6** | 6–9 | 19,7 |
| 9 | `157e0b93…` | green | 2026-08-26 | 70 | 1,50 | **6,7** | 6–9 | 20,0 |
| 10 | `90bf258c…` | green | 2026-09-17 | 70 | 1,48 | **6,8** | 5–11 | 20,2 |
| 11 | `3311e7fb…` | white | 2026-08-31 | 70 | 1,43 | **7,0** | 7–7 | 21,0 |
| 12 | `7d3007db…` | green | 2026-09-07 | 70 | 1,43 | **7,0** | 5–11 | 21,0 |
| 13 | `3d17bd15…` | white | 2026-09-30 | 50 | 4,21 | **7,1** | 5–11 | 11,9 |
| 14 | `a587ad61…` | brown | 2026-09-14 | 60 | 2,73 | **7,3** | 5–10 | 14,7 |
| 15 | `4abf4082…` | white | 2026-09-11 | 70 | 1,35 | **7,4** | 6–9 | 22,3 |
| 16 | `c1376b5e…` | green | 2026-09-16 | 70 | 1,27 | **7,9** | 7–8 | 23,6 |
| 17 | `f9a0dc4c…` | white | 2026-09-29 | 70 | 1,22 | **8,2** | 3–13 | 24,5 |
| 18 | `41c82d73…` | white | 2026-09-09 | 70 | 1,21 | **8,2** | 8–11 | 24,7 |
| 19 | `09a94ce5…` | green | 2026-09-21 | 70 | 1,19 | **8,4** | 7–12 | 25,2 |
| 20 | `95c562a8…` | white | 2026-08-27 | 70 | 1,19 | **8,4** | 8–9 | 25,3 |
| 21 | `0474cefc…` | green | 2026-09-21 | 60 | 2,31 | **8,7** | 8–82 | 17,3 |
| 22 | `0c6aa0da…` | white | 2026-08-19 | 70 | 1,15 | **8,7** | 6–16 | 26,0 |
| 23 | `96112372…` | white | 2026-09-17 | 70 | 1,13 | **8,9** | 5–15 | 26,6 |
| 24 | `441c3cac…` | green | 2026-09-22 | 60 | 2,26 | **8,9** | 5–62 | 17,7 |
| 25 | `f2f843bd…` | green | 2026-09-10 | 70 | 1,11 | **9,0** | 7–14 | 27,0 |

### Sensitivität: 75.-Perzentil-Rate statt Median

| Kennzahl | P25-Rate | Median-Rate | P75-Rate | Änderung P75 vs. Median |
|---|---|---|---|---|
| Median Tage bis 80% | 43,5 | 32,0 | **22,3** | −30% |
| Median Tage bis 100% | 81,3 | 58,1 | **41,9** | −28% |
| Reihen in 0–7 Tagen (bis 80%) | 7 | 12 | **30** | +150% |
| Reihen ≤30 Tage, nicht kritisch | 130 | 196 | **296** | +51% |

Die Arbeitsliste schwankt damit um Faktor 1,5, der Rang der obersten Reihen bleibt stabil:
7 der Top 10 (6 in allen drei Varianten) stehen in jeder Rate-Variante oben.

## Interpretation

- Ein Drittel des Bestands ist schon jetzt im kritischen Bereich; „Zeit bis 80%“ ist dort
  keine Planungsgröße mehr, sondern Nachweis eines bestehenden Rückstands.
- Die operative Menge ist klein: 12 Reihen in ≤7 Tagen, 64 in ≤14 Tagen. Das ist eine
  Tages- bis Zwei-Wochen-Liste, keine Flottenoptimierung.
- Braun ist das entspannteste Material (Median 98 Tage, nur 42 kritisch), Weiß das
  angespannteste (265 von 448 bereits ≥80%). Dringlichkeit folgt stark dem Material.
- Die Top-25 stehen fast alle bei 70% und laufen mit 1,1–2,2 pp/Tag weiter — Container,
  die in der nächsten Leerungsrunde sonst überlaufen.
- Die Spanne zeigt die echte Unsicherheit: bei `0474cefc…` und `441c3cac…` reicht sie von
  8 bis 82 bzw. 5 bis 62 Tagen, weil diese Reihen nur 1–2 positive Übergänge haben.

## Grenzen

- **Prognose, keine Messung.** Die Rate ist über den ganzen Zeitraum gemittelt;
  Saisonalität (Sommer, Weihnachten) wird nicht modelliert.
- **Lineare Fortschreibung** unterstellt konstantes Füllverhalten und keine Leerung.
  Leerung ist aber der Normalfall (41,1% aller Übergänge negativ) — die Zahl ist „Zeit bis
  zum Überlauf ohne Eingriff“, nicht „Zeit bis zum nächsten Leerungstermin“.
- **Stichtag ist die letzte Messung je Reihe**, nicht das Datenende: Median 2026-09-07,
  589 Reihen (44%) enden vor 2026-09-01, 43 vor 2026-06-01. Für alte Reihen ist der
  Startpunkt der Zählung veraltet, die Zeit bis 80% damit unterschätzt.
- **Kategoriale Auflösung** (10-pp-Stufen, `overfull` = 110) macht Raten grob; kurze
  Abstände erzeugen Ausreißer (Max 25 pp/Tag bei 2-Tage-Abstand, Reihe `b3a9f61a…`).
- **Fallback verzerrt:** 103 Reihen ohne positiven Übergang erhalten den Material-Median;
  sind sie real rückläufig, wird ihre Dringlichkeit überschätzt.
- 229 Messtage bei 1.338 Reihen heißt: Aggregate über Messtage beruhen auf wechselnden
  Teilmengen. `Location_id` ist ein Standort mit mehreren Behältern, kein einzelner
  physischer Container; Koordinaten sind synthetisch.
- Für belastbare Termine fehlen Leerungsereignisse (Datum, Menge), Behältervolumen und Adressen.

## Nächster Schritt

Die 12 Reihen mit ≤7 Tagen bis 80% (Plätze 1–12) als erste Leerungswelle festschreiben
und gegen die realen Leerungsdaten prüfen — erst dieser Abgleich zeigt, ob die lineare
Rate den Betrieb trifft.
