# 36 – Hypothesen für den Mentor formulieren

> Aus 35 Analysen destilliert: die CSV zeigt das *Verhalten* der Container,
> aber nicht *warum*. Die wichtigsten fehlenden Daten sind Standortstammdaten,
> Leerungsereignisse, Containerkapazitäten, Messprotokoll und Tourdaten.

## Frage

Welche zusätzlichen Daten braucht die Analyse, und was könnte man damit?

## Vorgehen

Sammlung aller Datenlücken, die in den Analysen 01–35 benannt wurden, dedupli-
ziert und priorisiert. Jede Lücke mit: was fehlt, warum es wichtig ist, welche
Analyse davon profitiert, und eine konkrete Frage an den Mentor.

## Ergebnisse

### Priorität 1 — Blocker für operative Nutzung

| # | Fehlende Daten | Warum wichtig | Profitiert | Frage an den Mentor |
|---|---|---|---|---|
| 1 | Echte Standortstammdaten (Adresse, Koordinaten, Stadtteil) | Ohne echte Koordinaten keine Route, keine räumliche Analyse | 24, 25, 26, 32, 34, 35 | Dürfen wir die echten Standortdaten für die 449 `Location_id` nutzen? |
| 2 | Leerungsereignisse (Datum, Volumen, Fahrzeug) | Nur dann sind Leerungen nicht mehr indirekt zu rekonstruieren; Kausalanalyse möglich | 16, 17, 21, 23, 27, 30 | Gibt es historische Leerungsdaten zu diesen Standorten? |
| 3 | Containerkapazitäten (Volumen, Größe, Aufstellung) | Trennung „zu klein" vs. „zu selten geleert" | 27, 28, 30, 35 | Welche Behältergrößen und Aufstellungen gibt es? |
| 4 | Messprotokoll (Auswahlregel, Frequenz, Feiertage) | Klärt, ob Messungen bedarfsgesteuert sind (Selektionsbias) | 18, 20, 29, 33 | Wie und wann werden Messungen ausgelöst? |
| 5 | Tour-/Fahrzeugdaten (Fahrzeuge, Kapazitäten, Servicezeiten) | Echte Routenoptimierung und Kostenrechnung | 24, 30, 31 | Welche Fahrzeuge, Kapazitäten und Servicezeiten nutzt PreZero? |

### Priorität 2 — Verstärker für Analysequalität

| # | Fehlende Daten | Warum wichtig | Profitiert | Frage |
|---|---|---|---|---|
| 6 | Wetterdaten (Temperatur, Niederschlag) | Test lokaler Treiber, saisonale Erklärung | 26, 11, 12 | Können wir Wetterdaten zu den Messtagen zuordnen? |
| 7 | Veranstaltungs-/Feiertagskalender | Erklärung von Anomalien | 15, 26, 12 | Gibt es einen Eventkalender für Heilbronn 2025/26? |
| 8 | Bevölkerungs-/Gebietsdaten (Zensus, OSM) | Erklärung von Standortunterschieden | 26, 25, 08 | Dürfen wir Open-Data-Quellen (Zensus, OSM) mit den Standorten verknüpfen? |
| 9 | Mehrjährige Daten (≥ 3 Jahre) | Saison und Trend trennen | 11, 12, 13, 21 | Gibt es Messdaten aus früheren Jahren? |
| 10 | Sensormetadaten (Typ, Kalibrierung, Ausfälle) | Datenqualität bewerten, Ausreißer erklären | 19, 15, 18 | Welche Sensoren werden verwendet und wie werden sie gewartet? |

### Priorität 3 — Nice-to-have

| # | Fehlende Daten | Warum wichtig | Profitiert |
|---|---|---|---|
| 11 | Haushalts-/Konsumstruktur je Gebiet | Erklärt Materialunterschiede | 06, 26, 28 |
| 12 | Konkurrenz-/Alternativstandorte (andere Sammelstellen) | Vollständiges Bild der Versorgung | 25, 32 |
| 13 | Kosten-/Preisdaten (Entsorgung, Transport) | Echte Kostenrechnung | 30, 31 |
| 14 | Feedback der Disponenten (akzeptierte/abgelehnte Vorschläge) | Lernen aus Entscheidungen | 23, 02 |

### Meta-Hypothese

Die wichtigste Erkenntnis aus 35 Analysen: **die CSV ist eine Messreihe von
Füllständen, keine Erhebung von Ursachen.** Jede kausale Aussage („dieser
Standort ist voll, weil…") ist eine Hypothese. Die CSV kann Verhalten
beschreiben und Prioritäten setzen, aber nicht erklären. Erst mit den Daten
aus Priorität 1 wird aus einer Füllstandsanalyse eine operative
Tourenentscheidung.

### Fragenliste für den Mentor (kompakt)

1. Dürfen wir echte Standortstammdaten für die 449 `Location_id` nutzen?
2. Gibt es historische Leerungsdaten zu diesen Standorten?
3. Welche Behältergrößen und Aufstellungen gibt es?
4. Wie und wann werden Messungen ausgelöst?
5. Welche Fahrzeuge, Kapazitäten und Servicezeiten nutzt PreZero?
6. Gibt es Messdaten aus früheren Jahren?
7. Dürfen wir Open-Data-Quellen mit den Standorten verknüpfen?

## Grenzen

Die Hypothesen sind aus der CSV abgeleitet, nicht aus Expertenwissen. Der
Mentor kann jede einzelne widerlegen oder bestätigen — das ist der Zweck
dieser Liste. Sie ist ein Gesprächsleitfaden, keine Anforderungsspezifikation.

## Nächster Schritt

Die sieben kompakten Fragen als Block an den PreZero-Mentor übergeben und die
Antworten als Datenvertrag für Phase 2 (Analyse 35) dokumentieren.