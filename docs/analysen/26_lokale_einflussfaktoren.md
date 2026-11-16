# 26 – Lokale Einflussfaktoren untersuchen

> Die CSV enthält keine Wetter-, Veranstaltungs- oder Geodaten. Was sie zeigen
> kann: Standorte verhalten sich gleichzeitig (Analyse 10, Median r = 0,66) —
> das ist ein Indiz für gemeinsame lokale Treiber, aber kein Beweis.

## Frage

Welche lokalen Faktoren könnten erklären, warum bestimmte Standorte stärker
ausgelastet sind — und wie ließe sich das testen?

## Vorgehen

Inventur möglicher Treiber, Hypothesen aus den vorhandenen Daten (ohne
externe Daten) und ein Testdesign für den Fall, dass Wetter-, Event- und
Geodaten nachgeliefert werden.

## Ergebnisse

### Indizien aus der vorhandenen CSV

| Beobachtung | Mögliche lokale Ursache | Datenlücke |
|---|---|---|
| Standorte mit allen drei Materialien gleichzeitig kritisch (137 im März) | Gemeinsames Einzugsgebiet, Haushaltsdichte | Keine Bevölkerungsdaten |
| Gleichsinnige Bewegung der drei Materialien am selben Standort (r = 0,66) | Gemeinsame Leerungszyklen oder lokale Treiber | Keine Leerungsdaten |
| Weiße Glasauslastung 44 pp höher als braune am selben Standort | Materialwahl der Haushalte, Verpackungsstruktur | Keine Konsumdaten |
| Standorte mit chronisch hohem Mittelwert (≥ 85 %) | Dichte Wohnbebauung, Gastronomie | Keine POI-/Gebietsdaten |
| Juni-Einbruch und März-Peak über alle Standorte | Saisonale Verhaltensänderung | Keine Wetterdaten |
| Anomalien an einzelnen Tagen (Analyse 15) | Veranstaltungen, Ferien, Betriebsstörungen | Keine Eventdaten |

### Hypothesen (zu testen, sobald Daten vorliegen)

1. **Haushaltsdichte** treibt die absolute Auslastung; Gewerbeanteil treibt
   Weißglas (Gastronomie → Flaschen).
2. **Entfernung zum Betriebshof** wirkt über Leerungsfrequenz, nicht über
   Nachfrage: weit entfernte Standorte werden seltener geleert und wirken
   voller.
3. **Wetter** (Temperatur, Niederschlag) beeinflusst Sammelverhalten —
   besonders im Winter (Heißgetränke → mehr Glas?).
4. **Schulen/Universitäten** erzeugen Spitzen in Semesterzeiten; Feiertage
   (Analyse 12) verschieben Leerungsrhythmen.
5. **Wochenend-/Wochentagseffekt** in der Messung selbst (Analyse 18: Sonntage
   nur 21 von 11.701 Messungen) — ein Messartefakt, der als Treiber
   missverstanden werden kann.

### Testdesign bei Anreicherung

- Regressionsmodell: Standortmittel (oder overfull-Rate) ~ Bevölkerung +
  Gewerbeanteil + POI-Dichte + Entfernung zum Hof + Material.
- Zeitliche Ebene: Tagesmittel ~ Wetter + Feiertagsindikator + Wochentag,
  mit Standort-Fixed-Effects.
- Kausale Absicherung über Fixed Effects und Placebo-Tests, weil die CSV
  keine randomisierte Variation enthält.

### Was die CSV allein NICHT kann

- Keine Kausalität: Korrelationen (z. B. Messhäufigkeit vs. Füllstand) sind
  durch Selektion und Material verzerrt (Analyse 20).
- Keine räumliche Analyse: ohne echte Koordinaten keine Nachbarschafts- oder
  Hotspot-Analyse.
- Keine Wetter-/Event-Zuordnung: die 229 Messtage lassen sich zwar mit
  externen Kalendern verknüpfen, aber ohne Leerungsdaten bleibt der Effekt
  unidentifizierbar.

## Grenzen

Jede „lokale Einflussfaktor"-Aussage aus dieser CSV ist eine Hypothese, kein
Befund. Die CSV ist eine Messreihe von Füllständen, keine Erhebung von
Ursachen. Tests ohne externe Daten wären Datenmining, keine Analyse.

## Nächster Schritt

Hypothesenliste (5 Punkte) dem Mentor als Datenanforderung übergeben; sobald
Wetter/Event/Geodaten vorliegen, eine erste Regressionsanalyse mit
Standort-Fixed-Effects als separaten Analyse-Schritt (26b) anlegen.