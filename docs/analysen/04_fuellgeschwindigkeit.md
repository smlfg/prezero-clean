# 04 – Füllgeschwindigkeit zwischen zwei Messungen

> Median-Zuwachs 0,74 Prozentpunkte pro Tag — aber die scheinbare Rate fällt mit dem Messabstand um Faktor 8 (1,91 pp/Tag bei 8–14 Tagen, 0,24 pp/Tag über 90 Tagen): zwischen zwei Messungen verschwinden Leerungen.

## Frage

Wie schnell füllt sich ein Container/Standort zwischen zwei Messungen wieder? Wie
verteilen sich die Raten nach Material und Zeitreihe — und verzerrt der Messabstand das Bild?

## Vorgehen

- Datenbasis: `../glass_fill_levels_anonymized_f.csv`, 11.701 Messungen, 2025-10-17 bis 2026-09-30; `overfull` als 110 % kodiert (tatsächliche Höhe unbekannt); keine Duplikate auf `(Location_id, material_type, date)`.
- Sortierung je Zeitreihe `(Location_id, material_type)` nach `date`; 1.338 Zeitreihen, davon 1.304 mit ≥ 2 Messungen. Je Paar: `Δ = fill_t − fill_{t−1}`, `dt` in Tagen, `Rate = Δ / dt`.
- **Nur positive Übergänge** (Δ > 0) zählen als Zuwachs; negative Δ = Leerung/Reset (Indiz, kein Beweis), Δ = 0 = unverändert — beide separat ausgewiesen.
- Kennzahlen n/Mittel/Median/Quartile/Klassen je Material und Abstandsband; Top-20 nur für Serien mit ≥ 3 positiven Übergängen (Rang nach Median-Rate).
- Zusammenhang Rate ↔ Abstand: Pearson und Spearman (numpy).

## Ergebnisse

**Übergangsbilanz (10.363 Paare)**

| Material | Übergänge | positiv | negativ | unverändert | Median-Abstand |
|---|---:|---:|---:|---:|---:|
| brown | 2.658 | 1.102 (41,5 %) | 1.033 (38,9 %) | 523 (19,7 %) | 33 d |
| green | 3.721 | 1.570 (42,2 %) | 1.631 (43,8 %) | 520 (14,0 %) | 27 d |
| white | 3.984 | 1.669 (41,9 %) | 1.602 (40,2 %) | 713 (17,9 %) | 27 d |
| **gesamt** | **10.363** | **4.341 (41,9 %)** | **4.266 (41,2 %)** | **1.756 (16,9 %)** | **28 d** |

**Raten der positiven Übergänge (n = 4.341, pp/Tag)**

| Kennzahl | Wert |
|---|---:|
| Mittel | 1,11 |
| Median | 0,74 |
| Q1 / Q3 | 0,38 / 1,43 |
| P90 / P95 / P99 | 2,35 / 3,16 / 5,68 |
| Min / Max | 0,04 / 25,00 |

Mittlerer Zuwachs je positivem Übergang: 30,5 pp (Median 20 pp), bei median 32 Tagen Abstand.

**Verteilung in Klassen (pp/Tag):** < 0,5 → 1.532 (35,3 %) · 0,5–1 → 1.171
(27,0 %) · 1–2 → 1.069 (24,6 %) · 2–3 → 326 (7,5 %) · > 3 → 243 (5,6 %).

**Raten je Material (positive Übergänge)**

| Material | n | Mittel | Q1 | Median | Q3 | Median-Δ | Tage von 0→100 bei Median-Rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| brown | 1.102 | 0,94 | 0,31 | 0,60 | 1,11 | 20 pp | 168 |
| green | 1.570 | 1,23 | 0,44 | 0,90 | 1,58 | 30 pp | 111 |
| white | 1.669 | 1,12 | 0,38 | 0,74 | 1,43 | 20 pp | 135 |

**Negative Übergänge (Leerung/Reset, n = 4.266)**

Median −30 pp (Q1 −40, Q3 −10, Extrem −100, Mittel −31,0). Betroffen: 1.247 von
1.304 Zeitreihen (95,6 %) haben mindestens einen negativen Sprung; 1.186 Serien
zeigen Zuwachs und Leerung im selben Verlauf.

**Rate und Beobachtungsabstand**

| Abstand (d) | n | Median-Rate | Mittel-Rate | Median-Δ |
|---|---:|---:|---:|---:|
| 1–7 | 66 | 4,29 | 5,47 | 20 pp |
| 8–14 | 340 | 1,91 | 2,34 | 20 pp |
| 15–21 | 687 | 1,33 | 1,62 | 20 pp |
| 22–28 | 745 | 1,07 | 1,22 | 30 pp |
| 29–42 | 1.167 | 0,67 | 0,84 | 20 pp |
| 43–60 | 600 | 0,58 | 0,66 | 30 pp |
| 61–90 | 437 | 0,35 | 0,44 | 30 pp |
| > 90 | 299 | 0,24 | 0,28 | 30 pp |

Pearson r = **−0,390** (p ≈ 3·10⁻¹⁷¹), Spearman ρ = **−0,613** (p < 0,001), n = 4.341.
Der Zähler (Median-Δ) bleibt über alle Abstandsklassen bei 20–30 pp konstant,
während die Rate um Faktor 8 sinkt.

**Top-20 Zeitreihen (≥ 3 positive Übergänge, `Location_id` auf 8 Zeichen gekürzt)**

| # | Location_id | Material | pos. Übergänge | Median-Rate | Max-Rate | Median-Abstand |
|---:|---|---|---:|---:|---:|---:|
| 1 | `20e4dd82` | white | 7 | 3,16 | 8,6 | 19 d |
| 2 | `20e4dd82` | green | 6 | 3,01 | 5,0 | 19 d |
| 3 | `9714654e` | brown | 12 | 2,93 | 8,6 | 12 d |
| 4 | `fdccb1ff` | brown | 9 | 2,86 | 7,5 | 18 d |
| 5 | `a587ad61` | brown | 9 | 2,73 | 7,1 | 20 d |
| 6 | `a587ad61` | green | 14 | 2,68 | 10,0 | 11 d |
| 7 | `5ff0f0b3` | white | 6 | 2,55 | 4,0 | 19 d |
| 8 | `9714654e` | green | 14 | 2,52 | 5,0 | 12 d |
| 9 | `1d4f4d33` | white | 7 | 2,50 | 6,9 | 13 d |
| 10 | `7947cea4` | brown | 3 | 2,38 | 3,2 | 42 d |
| 11 | `0786a63c` | white | 6 | 2,33 | 4,7 | 15 d |
| 12 | `5a80d4ab` | white | 4 | 2,33 | 3,2 | 24 d |
| 13 | `0474cefc` | green | 5 | 2,31 | 2,6 | 23 d |
| 14 | `09ad68b5` | green | 5 | 2,31 | 2,5 | 28 d |
| 15 | `441c3cac` | green | 4 | 2,26 | 4,3 | 22 d |
| 16 | `7843da14` | brown | 5 | 2,14 | 6,7 | 8 d |
| 17 | `8407541b` | white | 3 | 2,12 | 4,7 | 33 d |
| 18 | `695ce8a3` | green | 6 | 2,11 | 4,0 | 25 d |
| 19 | `eecbf6fa` | green | 12 | 2,11 | 6,2 | 13 d |
| 20 | `c3e031a4` | green | 6 | 2,07 | 4,4 | 14 d |

Auf Serienebene: 1.235 Zeitreihen mit ≥ 1 positivem Übergang, Median der
Serien-Medianrate 0,67 pp/Tag (Q3 1,05, Max 13,3); drei Standorte (`20e4dd82`,
`9714654e`, `a587ad61`) belegen mit je zwei Materialien sechs Top-20-Plätze.
21,7 % der positiven Übergänge enden bei `overfull` (110), ohne diese bleibt der
Median bei 0,74; nur 55 Übergänge (1,3 %) liegen über 5 pp/Tag.

## Interpretation

- **0,74 pp/Tag ist eine Untergrenze, keine Füllrate.** Die Rate ist bei kurzen
  Abständen 3–8× höher, obwohl der Median-Zuwachs konstant 20–30 pp bleibt — bei
  langen Abständen wird dazwischen geleert, die Messung sieht nur den Endstand.
  Realistischer Planungswert: Median 1,50 pp/Tag bei ≤ 21 Tagen (n = 1.093) = 67 statt 135 Tage von 0 auf 100.
- **Grün füllt sich am schnellsten**, braun am langsamsten (Median 0,90 vs.
  0,60 pp/Tag): braun ~168 Tage Nachfüllzyklus, grün ~111.
- **Leerungen dominieren das Signal.** 41,2 % aller Übergänge sind negativ, 95,6 %
  der Zeitreihen enthalten einen Reset, Median-Rücksprung −30 pp (drei Kategorien).
  Der Füllstand allein ist ein Sägezahn, kein Trend.
- Die Top-20-Serien (2,1–3,2 pp/Tag, Median-Abstände 8–20 Tage) sind plausibel
  stark frequentierte Standorte — prüfbar nur mit echten Adressen.

## Grenzen

- **Leerungen sind nicht protokolliert.** Ein positiver Übergang kann mehrere
  Leerungen enthalten; die Rate ist dann strukturell zu niedrig. Nur echte
  Leerungsereignisse (Zeitstempel, Menge) lösen das auf.
- **Die negative Korrelation ist teilweise definitorisch**: `Rate = Δ / dt`, `dt`
  steht im Nenner. Der belastbare Befund ist nicht der Koeffizient, sondern dass
  der Median-Zuwachs über alle Abstandsklassen bei 20–30 pp bleibt — der Zähler
  wächst also nicht mit dem Abstand mit.
- **Zensierung bei `overfull`**: 21,7 % der positiven Übergänge enden bei 110 %
  (als 110 kodiert, tatsächliche Höhe unbekannt). Für schnelle Serien ist die Rate
  nach oben abgeschnitten; das Ausmaß ist unbekannt.
- **Kategoriale Auflösung 10 pp** — die 66 Übergänge mit ≤ 7 Tagen sind deshalb grob.
- 34 Zeitreihen haben nur eine Messung; Messungen liegen an 229 Messtagen vor, Aggregate über Messtage sind durch die jeweils gemessene Teilmenge verzerrt. 449 `Location_id` sind Standorte, keine einzelnen Container — ein Mischbehälter verwischt die Rate je Material.

## Nächster Schritt

Alle Raten nur noch aus Übergängen mit ≤ 21 Tagen Abstand berechnen (n = 1.093,
Median 1,50 pp/Tag) und je Material gegen die 0,74 aus allen Abständen stellen,
damit der Planungswert die Leerungen nicht mehr mitzählt.
