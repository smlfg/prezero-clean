# 03 – Leerungsintervalle optimieren

> In 2.903 Messintervallen blieb ein Behälter durchgehend ≥80 % (Median 28 Tage); aus den beobachteten Steigraten folgt für 399 der 1.159 auswertbaren Zeitreihen ein kürzeres und für 546 ein längeres Leerungsintervall.

## Frage

Welche Container sollten häufiger, welche seltener geleert werden? Wie lang ist das beobachtete Intervall, in dem ein Behälter kritisch voll bleibt, und welches Intervall verträgt eine Zeitreihe bei ihrer gemessenen Füllrate?

## Vorgehen

- Datenbasis: `../glass_fill_levels_anonymized_f.csv`, 11.701 Messungen, 1.338 Standort-/Material-Zeitreihen; `overfull` als 110 % kodiert (tatsächliche Höhe unbekannt).
- **Kritische Paare:** zwei aufeinanderfolgende Messungen, beide ≥80 %. Deren Abstand ist das empirisch beobachtete „bleibt voll"-Intervall.
- **Unkritische Spannen:** aufeinanderfolgende Messungen, beide <80 %; je Serie das längste solche Intervall.
- **Füllrate:** nur steigende Paare (negative Sprünge = Indiz für Leerung, ausgeschlossen): Summe ΔFüllstand / Summe ΔTage.
- **Startniveau:** Median des Füllstands direkt nach einem Sprung < −5 Prozentpunkte (Fallback: Serienmittel, 13 Serien ohne Beleg).
- **Verträgliches Intervall** T80 = (80 − Startniveau) / Rate, begrenzt auf 7–365 Tage (35 Serien lagen darüber).
- **Segmentierung** über den Quotienten T80 / beobachteter Median-Messabstand: < 0,8 → verkürzen, > 1,25 → verlängern, sonst beibehalten.
- **Anfahrten** je Serie und Jahr: 365 / Abstand bzw. 365 / T80. Keine Kosten, nur Anfahrten.
- Auswertbar: 1.159 Serien (≥ 4 Messungen, Rate > 0). Ausgeschlossen 179 (13,4 %): 34 mit 1, 47 mit 2, 78 mit 3 Messungen.

## Ergebnisse

**Beobachtete kritische Intervalle** (2.903 von 10.363 Messpaaren = 28,0 %, aus 389 Serien):

| Kennzahl | Tage |
|---|---|
| Q1 | 20 |
| Median | 28 |
| Q3 | 42 |
| p90 | 64 |
| Max | 187 |

- 1.195 dieser Paare (41,2 %) enthalten mindestens eine `overfull`-Messung; Summe der kritischen Zeit 99.924 Tage.
- 527 Serien haben ≥ 2 kritische Intervalle; je Serie Median 35,5 Tage, Q3 56, p90 85, Max 187.

| Material | kritische Paare | Median | Q3 | Max |
|---|---|---|---|---|
| braun | 127 | 41 | 66 | 167 |
| grün | 901 | 29 | 42 | 178 |
| weiß | 1.875 | 27 | 40 | 187 |

**Längste Spanne ohne kritischen Wert** (1.035 Serien mit mindestens einem unkritischen Paar): Median 47 Tage, Q3 80, p90 134, Max 272. 20,7 % der Serien blieben über 90 Tage am Stück unkritisch. 172 Serien (14,8 %) erreichten nie 80 %; dort liegt der Median-Messabstand bei 45,5 Tagen und die längste unkritische Spanne bei 99,5 Tagen.

**Verträgliches Intervall vs. Beobachtung:** T80 Median 40,4 Tage (Q1 17,7 · Q3 87,1 · Mittel 67,4); beobachteter Median-Messabstand 33,5 Tage (Q1 24 · Q3 45,5). Bei 43,1 % aller Serien liegt T80 unter dem beobachteten Abstand.

| Segment | Serien | Anteil (auswertbar) | Anteil (alle 1.338) | Median T80 | Median Messabstand | Median Anteil ≥80 % |
|---|---|---|---|---|---|---|
| verkürzen | 399 | 34,4 % | 29,8 % | 11,3 d | 30 d | 66,7 % |
| beibehalten | 214 | 18,5 % | 16,0 % | 34,8 d | 34 d | 48,5 % |
| verlängern | 546 | 47,1 % | 40,8 % | 90,8 d | 35 d | 16,7 % |

| Material | verkürzen | beibehalten | verlängern |
|---|---|---|---|
| braun | 19 | 33 | 296 |
| grün | 123 | 98 | 180 |
| weiß | 257 | 83 | 70 |

**Beispiele** (IDs gekürzt, vollständige IDs in der CSV):

| Segment | Serie | Material | Messungen | Messabstand | T80 | Anteil ≥80 % | overfull-Anteil |
|---|---|---|---|---|---|---|---|
| verkürzen | `c347d4ef` | weiß | 8 | 27 d | 0 d | 100 % | 25 % |
| verkürzen | `ac8807de` | weiß | 8 | 40 d | 0 d | 100 % | 13 % |
| verkürzen | `2fd5400e` | weiß | 12 | 31 d | 0 d | 92 % | 25 % |
| beibehalten | `27627007` | grün | 16 | 25 d | 20 d | 56 % | 6 % |
| beibehalten | `2068fed4` | grün | 15 | 26,5 d | 31 d | 40 % | 0 % |
| beibehalten | `2b5245ce` | weiß | 14 | 25 d | 28 d | 50 % | 14 % |
| verlängern | `e5519892` | grün | 10 | 34 d | 62 d | 40 % | 0 % |
| verlängern | `73eac5c5` | braun | 8 | 45 d | 84 d | 12 % | 0 % |
| verlängern | `0ef4e394` | braun | 10 | 31 d | 58 d | 30 % | 0 % |

**Einsparung (Anfahrten, keine Kosten):** 546 Serien × Differenz 365/Abstand − 365/T80 ergibt **3.620 Anfahrten pro Jahr**; je Serie Median 5,8, Mittel 6,6, Max 30,9. Verteilung: braun 2.126, grün 1.164, weiß 330. Auf der Gegenseite brauchen die 399 verkürzen-Serien **8.185 zusätzliche Anfahrten pro Jahr** (weiß 5.895, grün 2.116, braun 174).

## Interpretation

- **Braun ist der klare Verlängerungsfall:** 85,1 % der Serien, T80-Median 92 Tage gegen 42 Tage Messabstand, Median-Füllstand 38 %, Median-Anteil ≥80 % nur 12 %. Hier ist die Frequenz etwa halbierbar.
- **Weiß ist der Verkürzungsfall:** 62,7 % der Serien, T80-Median 19 Tage gegen 33 Tage Abstand, 66 % der Messungen ≥80 %, 16,5 % `overfull`. Ein Teil der Serien ist dauerhaft voll (T80 = 0, weil das Startniveau nach der Leerung schon ≥80 % betrug).
- **Grün liegt dazwischen** und ist der einzige Fall, in dem ein pauschales Intervall je Material nicht trägt: 30,7 % verkürzen, 44,9 % verlängern.
- Die 3.620 eingesparten Anfahrten sind keine Nettoeinsparung: Der Zusatzbedarf von 8.185 Anfahrten ist rund doppelt so groß. Das Modell sagt also **Umschichtung**, nicht weniger Verkehr — und die Umschichtung trifft überwiegend weiß.
- Dass 43,1 % der Serien ein T80 unter ihrem Messabstand haben, passt zum `overfull`-Anteil von 10,2 %: Ein relevanter Teil der Behälter wird gemessen, wenn er schon voll ist.

## Grenzen

- **Leerungen sind nicht beobachtet.** Negative Sprünge (41,2 % aller Paare) werden als Leerung interpretiert; das ist ein Indiz, kein Beleg. T80 hängt direkt an dieser Annahme.
- **Kategoriale Skala:** 10-%-Schritte bedeuten bei einer Rate von 0,7 %/Tag rund ±7 Tage Unsicherheit je Grenzwert.
- **Quantisierung:** „≥80 % geblieben" heißt nur, dass zwei aufeinanderfolgende Messungen kritisch waren; die echte Dauer liegt zwischen einem Tag und dem Doppelten des Abstands.
- **Lineare Extrapolation** ignoriert Saisonalität, Feiertage und Füllverhalten; Serien starten zu unterschiedlichen Zeitpunkten im Jahr.
- **179 Serien (13,4 %) sind nicht auswertbar**; sie sind systematisch die dünn besetzten Zeitreihen, das Segmentbild ist also auf gut beobachtete Standorte verzerrt.
- 80 % ist eine gesetzte Schwelle, keine physikalische Kapazitätsgrenze; ohne Behältergröße, Adressen (Koordinaten sind synthetisch) und Tourenplanung sind keine echten Kilometer oder Kosten ableitbar.

## Nächster Schritt

Für die 546 verlängern-Serien die berechneten T80 gegen ein reales Leerungsprotokoll (Zeitstempel je Standort und Material) prüfen und daraus die 3.620 Anfahrten validieren, bevor Touren geändert werden.
