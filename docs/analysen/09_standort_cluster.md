# 09 – Standorte clustern

> k-Means findet vier Gruppen, aber die Trennung ist schwach (Silhouette 0,19): Die Standorte bilden eher ein Kontinuum mit einem harten Hochlast-Rand (31% der Standorte, mittlerer Füllstand 73%, 54% der Messungen ≥80%) als klar getrennte Typen.

## Frage

Lassen sich Standorte in Gruppen einteilen – „schnell voll“, „dauerhaft hoch ausgelastet“, „niedrige Nachfrage“, „unregelmäßig“ – oder ist das ein fließender Übergang? Und wie belastbar wäre eine solche Einteilung für die Tourenplanung?

## Vorgehen

- Datengrundlage: `../glass_fill_levels_anonymized_f.csv`, `overfull` als 110% kodiert (tatsächliche Höhe unbekannt). Aggregation je `Location_id` über alle Materialbehälter des Standorts.
- Filter: nur Standorte mit **≥8 Messungen** → **424 von 449** Standorten (11.589 von 11.701 Messungen, 99,0%).
- Feature-Matrix (6 Merkmale je Standort):
  - `f_mean`: mittlerer Füllstand (%)
  - `f_ge80`: Anteil Messungen ≥80%
  - `f_of`: Anteil `overfull`
  - `rate_pos`: Mittel der positiven Zuwächse je Tag (pp/Tag, nur Anstiege, Leerungen ausgeschlossen)
  - `gap_med`: Median des Messabstands in Tagen
  - `trans`: Anteil Messpaare, bei denen sich der Füllstand ändert (0–1) – Maß für Unregelmäßigkeit
- z-Standardisierung, k-Means (k-means++-Initialisierung, 25 Starts, beste Inertia), **k=3…6**; Silhouette als Auswahlkriterium. `scikit-learn` ist nicht installiert → eigene NumPy-Implementierung von k-Means und Silhouette (euklidisch, ohne Skalierungs-Sonderfälle). Das Ergebnis ist damit reproduzierbar, aber nicht gegen sklearn-Implementierungsdetails geprüft.
- Zusatzprüfungen: η² je Merkmal (Anteil erklärter Varianz), Merkmalskorrelationen, Robustheitslauf ohne die selten gemessenen Standorte.

## Ergebnisse

### Modellwahl

| k | Inertia | Silhouette | Cluster-Größen |
|---|---|---|---|
| 3 | 1546 | 0,180 | 140 / 115 / 169 |
| 4 | 1386 | **0,186** | 131 / 171 / 35 / 87 |
| 5 | 1247 | 0,186 | 116 / 101 / 29 / 96 / 82 |
| 6 | 1140 | 0,185 | 85 / 30 / 37 / 110 / 68 / 94 |

k=4 und k=5 sind praktisch gleichauf (Δ 0,0005, weit unter jeder sinnvollen Auflösung). **Gewählt: k=4** – es ist sparsamer, und k=5 spaltet nur das Hochlast-Cluster nach Anstiegsrate (1,44 vs. 0,86 pp/Tag) weiter auf.

### Cluster-Zentren in Original-Einheiten (k=4)

| Cluster | Name | n (%) | Ø Füllstand | Anteil ≥80% | overfull-Anteil | Rate pp/Tag | Messabstand (d) | Ø Messungen |
|---|---|---|---|---|---|---|---|---|
| 0 | **Hochlast – dauerhaft hoch, schnell wieder voll** | 131 (31%) | 72,9% | 0,54 | 0,17 | 1,30 | 27 | 37 |
| 1 | **Mittellast – Normalbetrieb** | 171 (40%) | 64,3% | 0,43 | 0,07 | 0,87 | 33 | 28 |
| 3 | **Niedriglast – wenig Nachfrage** | 87 (21%) | 51,2% | 0,23 | 0,03 | 0,61 | 46 | 18 |
| 2 | **Selten gemessen – Datenlücke, kein Nachfrage-Typ** | 35 (8%) | 59,0% | 0,37 | 0,03 | 0,34 | 95 | 11 |

Zum Vergleich alle 424 Standorte: 63,9% · 0,42 · 0,09 · 0,91 pp/Tag · 39 d.

### Material und Ausreißer

| Cluster | Grün | Weiß | Braun | Braun-Anteil | Standorte mit overfull-Anteil >20% |
|---|---|---|---|---|---|
| 0 Hochlast | 65 | 64 | 2 | 2% | 27% |
| 1 Mittellast | 83 | 80 | 8 | 5% | 2% |
| 3 Niedriglast | 43 | 40 | 4 | 5% | 0% |
| 2 selten gemessen | 13 | 14 | 8 | **23%** | 0% |

Kein Material dominiert einen Cluster flächendeckend; braune Behälter sind nur in der „selten gemessen“-Gruppe überrepräsentiert (23% vs. 5,2% gesamt) – ein Hinweis auf Messlogistik, nicht auf Nachfrage.

**Top-Beispiele je Cluster (Standort-IDs gekürzt, volle ID in der CSV):**

- Hochlast: `d5be6df1…` (91,7%, 0,80 ≥80%, Rate 0,89) · `83086ae1…` (87,8%, 0,80, 0,77) · `80b7f22a…` (87,0%, 0,70, 0,42 overfull, Rate 1,64)
- Mittellast: `06209e37…` (80,0%, 0,65, 0,81) · `c841c86b…` (75,8%, 0,58, 0,73) · `3eebdc41…` (75,7%, 0,52, 0,80)
- Niedriglast: `4fa2e066…` (65,0%, 0,36) · `3311e7fb…` (63,1%, 0,23) · `e7ccc298…` (62,3%, 0,31)
- Selten gemessen: `975d7c3e…` (81,0%, Abstand 124 d) · `da44e4a1…` (79,2%, 96 d) · `d8393c4c…` (69,3%, 72 d)

### Wie gut trennt das wirklich?

- **Silhouette 0,186** heißt nach gängiger Lesart: „keine substanzielle Struktur“ (<0,25). Die Cluster sind eine grobe Sortierung, keine Klassen.
- η² je Merkmal: Messabstand 0,65 · Füllstand 0,64 · Anteil ≥80% 0,60 · overfull 0,49 · Rate 0,30 · **Unregelmäßigkeit 0,05**.
- Füllstand und Anteil ≥80% korrelieren mit 0,92 – das ist faktisch ein Merkmal, nicht zwei.
- Verteilung des mittleren Füllstands ist eingipflig (14 / 39 / 140 / 153 / 70 / 8 Standorte in sechs gleich breiten Klassen), kein Doppelpeak.
- Cluster-Größen sind starter-abhängig: andere Startwerte liefern Verteilungen wie 102/105/106/111 oder 35/90/132/167. Stabil ist nur der Hochlast-Rand und die selten gemessene Gruppe.
- Robustheit ohne die 39 Standorte mit Median-Messabstand ≥70 Tage (davon 31 in Cluster 2): k=2 erreicht Silhouette **0,270** – der bestgetrennte Schnitt ist also „hoch vs. niedrig“, nicht vier Typen.

## Interpretation

- **„Dauerhaft hoch ausgelastet“ ist belegbar, „schnell voll“ nur als Variante davon.** Cluster 0 vereint hohes Niveau (73%) mit hoher Anstiegsrate (1,30 pp/Tag) und überdurchschnittlichem overfull-Anteil (17%). Bei k=5 zerfällt er in einen schnellen (1,44 pp/Tag, 74% Füllstand) und einen langsameren Teil (0,86 pp/Tag, 66%).
- **„Niedrige Nachfrage“ ist belegbar** (21% der Standorte, 51%, nur 23% ≥80%, 3% overfull) – das ist die Gruppe, bei der eine Intervallstreckung am wenigsten Risiko trägt.
- **„Unregelmäßig“ ist kein Clustertyp.** Fast alle Standorte sind unregelmäßig: im Median ändern sich 84% aller Messpaare im Füllstand. Das liegt an 10%-Stufen, Leerungen und langen Messabständen, nicht an einem Standortmuster (η² 0,05).
- **Der Cluster „selten gemessen“ ist ein Datenartefakt, kein Betriebstyp.** Abstand 95 Tage, Rate 0,34 pp/Tag: Wer nur alle drei Monate gemessen wird, hat zwangsläufig wenige, über lange Zeiträume gemittelte Anstiege. Diese 35 Standorte sollten vor jeder Einordnung nachgemessen werden.
- Für die Planung: Die 131 Hochlast-Standorte (bzw. 57 mit Füllstand ≥70% und Rate ≥1,0 pp/Tag) sind die Kandidaten für feste kurze Intervalle, die 87 Niedriglast-Standorte für Streckung. 63 Standorte (14,9%) erfüllen gleichzeitig ≥50% ≥80% und Rate ≥1,0 – das ist die eigentliche Engpassliste.

## Grenzen

- Silhouette 0,19: Die Cluster sind **nicht** als diskrete Klassen zu lesen. Jede harte Zuweisung („Standort X ist Typ Y“) überzeichnet die Daten; sinnvoller ist ein Score statt einer Klasse.
- Messabstand ist standortabhängig (Median 39 d, Spanne 7–147 d). Clustergrenzen verschieben sich dadurch; die „Rate“ ist bei wenigen Messungen stark verrauscht.
- `fill_level_perc` ist kategorial (10%-Stufen), `overfull` = 110% ist eine Setzung – echte Überläufe und Füllhöhen über 100% sind unbekannt.
- Leerungen sind nicht protokolliert; negative Sprünge werden als Leerung interpretiert. Ohne Leerungsdaten ist „Nachfrage“ nur indirekt aus Anstiegen ableitbar.
- Standorte bündeln bis zu drei Materialbehälter (Median 3); ein hoher Standortmittelwert kann aus einem einzelnen weißen Behälter stammen.
- Aggregate über Messtage sind durch die je Tag gemessene Teilmenge verzerrt; Koordinaten sind synthetisch, also keine räumliche/cluster-geografische Aussage möglich.
- k-Means unterstellt kugelige, etwa gleich große Cluster. Die starter-abhängigen Größen zeigen, dass diese Annahme hier schwach trägt.

## Nächster Schritt

Für die 35 Standorte mit Messabstand ≥70 Tage einen Nachmess-Zyklus einplanen – erst danach ist die Clusterzuordnung dieser Gruppe belastbar und die 4er-Einteilung als Planungsgrundlage verwendbar.
