# 28 – Containergrößen oder Aufstellorte bewerten

> Weißglas ist an 359 von 441 Standorten (81 %) im Mittel mehr als 30 pp
> voller als Braunglas am selben Standort. Die Auslastungsdifferenz ist damit
> ein Materialproblem, kein Standortproblem — Behältergrößen sollten
> materialabhängig geplant werden.

## Frage

Zeigen Unterschiede in der Auslastung, ob vorhandene Kapazitäten am jeweiligen
Standort angemessen sind?

## Vorgehen

Materialvergleich auf Standortebene (gepaart), chronisch hohe Zeitreihen
(Mittelwert ≥ 85 %) je Material, und Prüfung, ob Auslastungsunterschiede
standortspezifisch oder materialspezifisch sind. Hinweis: Containergrößen
liegen nicht in der CSV — die Analyse bewertet nur die Auslastungsmuster.

## Ergebnisse

### Gepaarter Vergleich am selben Standort (441 Standorte mit allen drei Materialien)

| Vergleich | Standorte mit A > B | Median-Differenz (pp) |
|---|---:|---:|
| Weiß > Braun | 429 (97,3 %) | +44,0 |
| Grün > Braun | 408 (92,5 %) | +26,0 |
| Weiß > Grün | 393 (89,1 %) | +16,0 |

Die Rangfolge Weiß > Grün > Braun gilt an fast jedem Standort. Der Unterschied
ist ein Materialeffekt, kein Standorteffekt.

### Chronisch hohe Zeitreihen (Mittelwert ≥ 85 %)

| Material | Zeitreihen gesamt | davon mean ≥ 85 % | Anteil |
|---|---:|---:|---:|
| brown | 449 | 3 | 0,7 % |
| green | 449 | 32 | 7,1 % |
| white | 449 | 173 | 38,5 % |

173 von 449 Weiße-Glas-Zeitreihen (38,5 %) sind chronisch über 85 % — bei
Braunglas sind es 3. Das ist der stärkste Hinweis, dass Weißglas-Behälter
am selben Standort zu klein (oder zu selten geleert) sind.

### Auslastungsklassen je Material (Standortmittel)

| Material | Standorte < 50 % | 50–79 % | ≥ 80 % |
|---|---:|---:|---:|
| brown | 312 (69,5 %) | 116 (25,8 %) | 21 (4,7 %) |
| green | 74 (16,5 %) | 231 (51,4 %) | 144 (32,1 %) |
| white | 28 (6,2 %) | 140 (31,3 %) | 281 (62,6 %) |

### Aufstellorte (Standorte mit allen drei Materialien)

- 441 von 449 Standorte (98,2 %) haben alle drei Materialien — das ist das
  typische Aufstellungsmuster „drei Behälter nebeneinander".
- Nur 8 Standorte haben weniger als drei Materialien (2 mit zwei, 1 mit einem).
- An Standorten mit drei Behältern ist der Weiße-Glas-Behälter fast immer der
  kritischste (97,3 % der Fälle, s. o.).

### Interpretation für Containergrößen

- **Materialabhängige Größenplanung:** Weißglas-Behälter sollten am selben
  Standort größer sein als Braun-/Grün-Behälter — oder häufiger geleert werden.
- **Aufstellort an sich ist nicht das Problem:** die drei Behälter stehen am
  gleichen Ort, aber einer (Weiß) ist chronisch überlastet. Eine Vergrößerung
  nur des Weiße-Glas-Behälters (oder ein zusätzlicher Behälter) wäre die
  zielgenaueste Maßnahme.
- **Braunglas-Behälter sind oft überdimensioniert:** 69,5 % der Standorte
  liegen unter 50 % — Kandidaten für kleinere Behälter oder Bündelung
  (Einsparpotenzial, Analyse 31).

## Grenzen

Ohne Containergröße, Aufstellort (einzelner Behälter vs. Containergruppe) und
Leerungshistorie kann nicht unterschieden werden, ob ein voller Behälter
zu klein ist oder zu selten geleert wird. Die CSV zeigt nur das Ergebnis
(Füllstand), nicht die Kapazität. Zwei Standorte mit identischem Füllstand
können völlig unterschiedliche Behältergrößen haben.

## Nächster Schritt

Containerstammdaten (Größe, Aufstellung, Leerungsvolumen) von PreZero
erfragen und mit Klasse A aus Analyse 27 abgleichen: dort, wo ein
Weißglas-Behälter chronisch ≥ 85 % ist und die Größe unter dem Standortmedian
liegt, ist eine Vergrößerung die naheliegende Maßnahme.