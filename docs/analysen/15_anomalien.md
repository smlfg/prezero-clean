# 15 – Anomalien erkennen

> 1.357 der 10.363 Messwert-Übergänge (13,1 %) springen um mehr als 40 pp nach oben oder mehr als 60 pp nach unten, und 333 Messungen (3,1 %) sind Ausreißer gegenüber ihrer eigenen Zeitreihe – die Sprünge sind überwiegend Beobachtungslücken (Median-Abstand 41 Tage), keine beobachteten Ereignisse.

## Frage

Welche ungewöhnlichen Werte, Sprünge und Ausreißer gibt es, wie häufig sind sie, wo liegen sie – und
was könnten sie bedeuten (Leerung, Fehlmessung, Sensorreset, Veranstaltung)?

## Vorgehen

- Daten: `glass_fill_levels_anonymized_f.csv`, 11.701 Messungen, 1.338 Standort-Material-Zeitreihen, 2025-10-17 bis 2026-09-30; `overfull` = 110 % kodiert (tatsächliche Höhe unbekannt).
- **(a) Ausreißer:** je Zeitreihe mod. Z-Score `0,6745 · (x − Median) / MAD`, Schwelle |Z| > 3,5. Reihen mit MAD = 0 (164 Reihen, 804 Messungen) sind nicht bewertbar → 1.174 bewertbare Reihen mit 10.897 Messungen.
- **(b) Sprünge:** Differenz aufeinanderfolgender Messungen je Zeitreihe; positiv > +40 pp, negativ < −60 pp.
- **(c) Volatilität:** SD je Zeitreihe (n ≥ 2) > 40 pp; **(d) Widersprüche:** Dreierfolge `overfull → ≤ 40 % → overfull`, implizite Füllrate gegen Median-Zuwachs (0,57 pp/Tag, p99 = 3,69 pp/Tag).
- **(e)** alle Messungen mit 0 %; **(f)** Tagesmittel an Messtagen mit ≥ 30 Messungen (191 von 229 Tagen).

## Ergebnisse

### (a) Ausreißer je Zeitreihe (mod. Z > 3,5)

333 Ausreißer in 244 von 1.174 Reihen (20,8 %), fast symmetrisch (167 positiv, 166 negativ), 48 davon
`overfull` und 56 bei 100 %. Anteile: braun 128 von 2.621 (4,9 %), weiß 130 von 4.243 (3,1 %),
grün 75 von 4.033 (1,9 %). Schwerpunkt **Juni 2026: 97 Ausreißer (29,1 %)**, dann April/Mai (43/42).

| Datum | Standort | Mat. | Wert | Reihen-Median (MAD) | Z |
|---|---|---|---|---:|---:|
| 2026-05-05 | f944c52b | brown | overfull | 15 (5) | +12,8 |
| 2026-05-15 | dbe5e31c | brown | overfull | 20 (5) | +12,1 |
| 2026-05-20 | 090a084c | brown | 100 | 20 (5) | +10,8 |
| 2026-07-02 | 734f7e77 | white | 10 | 100 (5) | −12,1 |

### (b) Große Sprünge

Positive Sprünge > +40 pp: **983**; negative < −60 pp: **374**; zusammen 13,1 % aller Übergänge.
Beträge sind reine Vielfache von 10 pp (+50: 377, +60: 268, +70: 179, +80: 96, +90: 47, +100: 16;
−70: 203, −80: 114, −90: 46, −100: 11) – Zwischengrößen fehlen, Folge der kategorialen Skala.
Anteil an allen Übergängen: braun 14,7 %, grün 14,0 %, weiß 11,2 %. Median-Abstand 21 Tage (negativ)
bzw. 35 Tage (positiv), Minimum 1 Tag. 754 von 1.338 Reihen haben mindestens einen Sprung (Spitze:
9714654e braun, 9). Bis März 2026 bleiben die Monatswerte bei 26–104 Sprüngen, zu 90–96 % positiv.

| Monat | Sprünge | positiv | negativ |
|---|---:|---:|---:|
| 2026-04 | 136 | 108 | 28 |
| 2026-05 | 176 | 105 | 71 |
| 2026-06 | 191 | 70 | 121 |
| 2026-07 | 254 | 202 | 52 |
| 2026-08 | 145 | 104 | 41 |
| 2026-09 | 111 | 91 | 20 |

**Top 20 nach Betrag (bei Gleichstand kürzester Abstand):**

| Datum | Standort | Mat. | von → nach | Δ | Tage |
|---|---|---|---|---:|---:|
| 2026-06-16 | 0004c095 | white | 110 → 10 | −100 | 7 |
| 2026-06-17 | 9e917a1b | white | 110 → 10 | −100 | 16 |
| 2026-09-21 | 7d695986 | white | 10 → 110 | +100 | 18 |
| 2026-09-29 | 1e82edc0 | brown | 10 → 110 | +100 | 19 |
| 2026-07-15 | 3412c5d4 | white | 10 → 110 | +100 | 21 |
| 2026-08-31 | 09b56d50 | white | 110 → 10 | −100 | 27 |
| 2026-09-30 | 5bdc5e59 | white | 10 → 110 | +100 | 30 |
| 2026-01-12 | 9dc40dd4 | brown | 10 → 110 | +100 | 31 |
| 2026-06-06 | f944c52b | brown | 110 → 10 | −100 | 32 |
| 2026-06-25 | 09b56d50 | brown | 10 → 110 | +100 | 35 |
| 2026-07-02 | 734f7e77 | white | 110 → 10 | −100 | 35 |
| 2026-02-27 | 4a6680af | brown | 10 → 110 | +100 | 36 |
| 2026-09-29 | cb52636c | brown | 10 → 110 | +100 | 40 |
| 2026-01-29 | 7947cea4 | brown | 10 → 110 | +100 | 42 |
| 2026-07-03 | a82eb896 | brown | 110 → 10 | −100 | 49 |
| 2026-07-24 | 1cdc8b7e | white | 110 → 10 | −100 | 55 |
| 2026-09-29 | a6e674b2 | brown | 10 → 110 | +100 | 55 |
| 2026-02-25 | 5ff0f0b3 | brown | 10 → 110 | +100 | 64 |
| 2026-07-22 | 4f33f7dd | brown | 110 → 10 | −100 | 65 |
| 2026-07-22 | 8407541b | brown | 110 → 10 | −100 | 68 |

### (c) Extrem volatile Zeitreihen (SD > 40 pp)

32 von 1.304 Reihen (2,5 %): braun 19, weiß 7, grün 6. **Alle sind Kurzreihen** – Median n = 3,5,
Maximum n = 12, nur 6 Reihen mit ≥ 5 Messungen (Extremfall 67634892 braun: 2 Messungen, 10 % →
overfull, SD 70,7 pp). Die Volatilität ist Artefakt weniger Leerungen, kein dauerhaft schwankender Behälter.

### (d) Widersprüchliche Verläufe: `overfull → ≤ 40 % → overfull`

14 Fälle in 14 Reihen (9dc40dd4 zweimal, je Material):

| Standort | Mat. | overfull | Zwischenwert | overfull | implizite Füllrate |
|---|---|---|---:|---|---:|
| 0e2e0c4c | white | 2026-03-04 | 30 | 2026-04-15 | 5,0 pp/Tag |
| cf3c2e1a | white | 2026-04-30 | 30 | 2026-05-29 | 5,0 pp/Tag |
| 05c3c6dc | white | 2026-04-22 | 40 | 2026-05-15 | 4,7 pp/Tag |
| 5121497c | white | 2026-02-25 | 40 | 2026-03-19 | 4,1 pp/Tag |
| 9dc40dd4 | green | 2026-04-29 | 20 | 2026-05-29 | 3,6 pp/Tag |

Weitere 9 Fälle liegen mit 1,0–3,2 pp/Tag im normalen Bereich; vier überschreiten den p99-Zuwachs
(3,69 pp/Tag). 213 Messungen folgen direkt auf `overfull → overfull` (plausibel ohne Leerung), 48-mal
folgt auf `overfull` ein Wert ≤ 20 %.

### (e) Die zwei 0-%-Messungen

- **a587ad61, green, 2025-12-11:** zwischen 60 % (2025-12-04) und 50 % (2025-12-16); 0 → 50 % in 5 Tagen
  entspricht 10 pp/Tag (26× Median) – **unplausibel, Fehlmessung wahrscheinlich**.
- **c5f40f51, brown, 2026-06-12:** zwischen zwei 10-%-Werten (2026-01-20, 2026-08-13) – **plausibel
  als fast leerer Behälter**.

### (f) Auffällige Messtage (≥ 30 Messungen, 191 Tage)

Tagesmittel im Schnitt 66,4 %, SD 13,2 pp.

| Tag | Messungen | Ø | overfull-Anteil | ≥ 80 % |
|---|---:|---:|---:|---:|
| 2026-03-05 | 49 | 100,4 % | 67,3 % | 87,8 % |
| 2026-03-06 | 50 | 99,8 % | 64,0 % | 88,0 % |
| 2026-03-04 | 35 | 95,4 % | 60,0 % | 85,7 % |
| 2026-03-11 | 50 | 93,4 % | 46,0 % | 88,0 % |
| 2026-06-22 | 40 | 34,8 % | 0,0 % | 7,5 % |
| 2026-06-12 | 75 | 37,2 % | 0,0 % | 8,0 % |

Der Spitzentag 2026-03-05 entsteht fast vollständig aus der overfull-Kodierung; höchste Einzelzahl: 60 overfull an einem Tag (2026-05-15, 117 Messungen).

## Interpretation

- **Leerung (Muster belegt, Ereignis nicht):** 374 Sprünge < −60 pp und 48-mal `overfull → ≤ 20 %` sind das erwartbare Signal; bei 41 Tagen Median-Abstand sieht man fast nie die Leerung, nur ihr Ergebnis.
- **Fehlmessung/Sensorreset (vermutet):** 111 der 153 negativen Ausreißer mit Folgemessung liegen wieder
  ±10 pp um den Reihen-Median; die 0-%-Messung mit 10 pp/Tag Rücklauf; 164 Reihen mit MAD = 0.
- **Veranstaltung/Saison (unbelegt):** Block 2026-03-04 bis 03-06 und Juni-Tiefpunkt (34,8–44,7 %)
  sind die stärksten Ausschläge; ohne Veranstaltungs-, Wetter- und Leerungsdaten bleibt es offen.

## Grenzen

- 10-pp-Skala: Sprünge unter 40 pp sind nicht messbar; die Klassengrenzen sind gesetzt, nicht aus den
  Daten abgeleitet. `overfull` = 110 ist Setzung – Sprünge von/zu overfull sind unterschätzt.
- MAD = 0 in 164 Reihen: gerade die konstanten (vermutlich defekten) Reihen fallen aus der Prüfung
  heraus; 333 Ausreißer sind eine Untergrenze.
- Kausalität: „Leerung“, „Fehlmessung“, „Veranstaltung“ sind Post-hoc-Deutungen. Es fehlen
  Leerungsprotokolle, Sensor-/Batteriestatus, Wetter und Veranstaltungskalender.
- Tagesaggregate (f) sind durch die tagesabhängige Mess-Teilmenge verzerrt; Koordinaten synthetisch.

## Nächster Schritt

Plausibilitätsfilter bauen (zwischen zwei Leerungen monoton steigend, max. 3,69 pp/Tag = p99), beziffern wie viele der 11.701 Messungen unplausibel sind, dann Füllraten neu rechnen.
