# 32 – Pilotgebiete vergleichen

> Die 449 Standorte lassen sich in vier Gruppen einteilen: 119 hochlast-stabil,
> 107 hochlast-volatil, 105 niedrig-stabil, 118 niedrig-volatil. Die Gruppen
> unterscheiden sich in Auslastung (52,6 % vs. 73,7 %) und overfull-Rate
> (3 % vs. 12 %) — aber die Trennung ist moderat, das Verhalten liegt auf
> einem Kontinuum.

## Frage

Welche Standortgruppen eignen sich für einen Pilotversuch?

## Vorgehen

Klassifikation der 449 Standorte nach zwei Merkmalen: mittlerer Füllstand
und Variabilität (Standardabweichung der Messwerte). Vier Quadranten.
Charakterisierung je Gruppe: Auslastung, Volatilität, overfull-Rate,
Messhäufigkeit. Empfehlung, welche Gruppe für welchen Pilotversuch geeignet ist.

## Ergebnisse

### Vier Standortgruppen (Median-Split nach Mittelwert und SD)

| Gruppe | n | Mittlerer Füllstand | SD | overfull-Rate | Messungen |
|---|---:|---:|---:|---:|---:|
| Hochlast-stabil | 119 | 73,7 % | 27,1 pp | 12 % | 30,5 |
| Hochlast-volatil | 107 | 69,5 % | 33,0 pp | 13 % | 27,4 |
| Niedrig-stabil | 105 | 52,6 % | 26,5 pp | 3 % | 24,2 |
| Niedrig-volatil | 118 | 58,0 % | 33,6 pp | 8 % | 22,0 |

### Charakterisierung

- **Hochlast-stabil (119):** die besten Pilotkandidaten für engere Intervalle —
  hohe Auslastung, vorhersagbares Verhalten, geringe Volatilität.
- **Hochlast-volatil (107):** Kandidaten für dynamische Prognose und
  bedarfsgesteuerte Touren — hohe Auslastung, aber unregelmäßig.
- **Niedrig-stabil (105):** Kandidaten für verlängerte Intervalle oder
  Bündelung — niedrige Auslastung, vorhersagbar.
- **Niedrig-volatil (118):** Kandidaten für Kapazitätsreduktion oder
  Standortzusammenlegung — niedrige Auslastung, unregelmäßig.

### Empfehlung für Pilotgebiete

| Pilotziel | Geeignete Gruppe | Begründung |
|---|---|---|
| Engere Intervalle testen | Hochlast-stabil | Vorhersagbar, hohes Einsparpotenzial bei Überfüllung |
| Dynamische Prognose testen | Hochlast-volatil | Hier zeigt sich, ob Prognose unsichere Standorte besser priorisiert |
| Intervalle verlängern testen | Niedrig-stabil | Geringes Risiko, klare Einsparung |
| Kapazitätsmaßnahmen (größere Behälter) | Hochlast-stabil + Hochlast-volatil | Beide haben die höchste overfull-Rate |

### Vergleichbarkeit der Gruppen

Die Gruppen sind über Median-Split gebildet und nicht clusterbasiert. Die
Standardabweichung variiert nur wenig (26,5–33,6 pp) — die Trennung ist
moderat und das Verhalten liegt auf einem Kontinuum (Analyse 09). Für einen
echten Pilotvergleich sollte man Standorte mit ähnlicher Messhäufigkeit und
gleichem Materialmix wählen, um Confounder zu kontrollieren.

## Grenzen

Ohne echte Koordinaten kann keine geografisch zusammenhängende Pilotregion
definiert werden — die vier Gruppen sind statistische Segmente, keine
Gebiete. Die Klassifikation nutzt nur den Mittelwert und die SD; andere
Merkmale (Messhäufigkeit, Materialmix, Saisonalität) sind nicht kontrolliert.
Die Gruppen sind nicht stabil über die Zeit (Analyse 08: Rangkorrelation
zwischen Halbjahren nur 0,30).

## Nächster Schritt

Pilotgruppen (je 10–20 Standorte) aus der Hochlast-stabil-Gruppe auswählen,
mit dem Mentor abstimmen und als A/B-Test (neue Intervalle vs. Status quo)
über einen Quartal laufen lassen, sobald echte Leerungsdaten vorliegen.