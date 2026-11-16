# Puffer-Modell (`src/modell.py`) und Bilanztest (`tests/test_bilanz.py`)

Grundlage ist `docs/datenmodell.md`. Alle Zahlen in diesem Dokument stammen aus `data/raw/glass_fill_levels_anonymized_f.csv` und sind über `scripts/fakten.py` berechnet und belegt.

---

## 1. Modellformel (Container als Puffer)

Jeder physische Container ist durch das Paar $c = (\text{Location\_id}, \text{material\_type})$ bestimmt (**1.338** Container an **449** Standorten; `fakten.py` Abschnitt 3).

Für die zeitlich geordneten Messungen $t_{c,0} < t_{c,1} < \dots < t_{c,m_c}$ eines Containers $c$ gilt:

1. **Besuchsabstand (in Tagen):**
   $$\Delta t_{c,k} = t_{c,k} - t_{c,k-1} \quad (\text{für } k \ge 1,\; \Delta t_{c,k} \ge 1\text{ Tag})$$
   Die jeweils erste Messung $k = 0$ jedes Containers (**1.338** Zeilen) besitzt keinen Vorgänger; für die Bilanz bleiben **10.363** Folgemessungen (`abstand > 0`, `fakten.py` Abschnitt 5 & 6).

2. **Abfluss (Leerung bei Messung):**
   Unmittelbar nach jeder Messung wird der Puffer auf $0\,\%$ geleert (Annahme A1 & A4):
   $$F_c(t_{c,k-1}^+) = 0\,\%$$

3. **Zufluss (tägliches Wachstum in % pro Tag):**
   Zwischen $t_{c,k-1}$ und $t_{c,k}$ fließt täglich die konstante Füllrate $r_c \ge 0$ (`% / Tag`, Annahme A2) zu. Vor der Leerung bei $t_{c,k}$ beträgt der ungedeckelte Pufferstand:
   $$\hat{y}_{c,k} = r_c \cdot \Delta t_{c,k}$$
   Auf der numerischen Messskala $[0, 100]$ (`fakten.py` Abschnitt 2) lautet die gedeckelte Vorhersage:
   $$\hat{p}_{c,k} = \min\!\big(r_c \cdot \Delta t_{c,k},\; 100\big)$$

4. **Schätzung der Füllrate $r_c$ mit rechtszensiertem `'overfull'` ($\ge 100\,\%$, nicht als `100`):**
   - **Unzensierte Folgemessungen** (`fill_level_perc != 'overfull'`, **9.206** Zeilen; `fakten.py` Abschnitt 6):
     Aus dem gemessenen Stand $p_{c,k} \in \{0, 10, \dots, 100\}$ wird das tägliche Wachstum berechnet:
     $$r_{c,k} = \frac{p_{c,k}}{\Delta t_{c,k}} \quad (\%/\text{Tag})$$
     und je Container als robuster Median aggregiert:
     $$r_c^{\text{unc}} = \text{Median}_{k \in \text{unzensiert}(c)}\!\left(\frac{p_{c,k}}{\Delta t_{c,k}}\right)$$
   - **Rechtszensierte Folgemessungen** (`fill_level_perc == 'overfull'`, **1.157** Folgemessungen; weitere **35** `'overfull'`-Zeilen liegen bei Erstmessungen ohne Vorgänger, zusammen **1.192** Zeilen = **10,2 %**; `fakten.py` Abschnitt 2 & 6):
     Der wahre Füllstand liegt bei $y_{c,k} \ge 100\,\%$ (Annahme A3). `'overfull'` wird **nicht** als Zahlenwert `100` in $r_c^{\text{unc}}$ eingesetzt (das würde die Rate bei langen Intervallen systematisch nach unten verzerren), sondern liefert eine untere Schranke für die Rate im Intervall:
     $$r_{c,k} \ge r_{c,k}^{\min} = \frac{100}{\Delta t_{c,k}}$$
     Für die **1.303** Container mit unzensierten Folgemessungen gilt $r_c = r_c^{\text{unc}}$; für den **1** Container, der ausschließlich eine `'overfull'`-Folgemessung besitzt, wird die zensierte Untergrenze $\text{Median}(r_{c,k}^{\min})$ als Mindestrate verwendet (zusammen **1.304** Container mit Rate; **34** Container haben im gesamten Zeitraum nur 1 Messung ohne Folgemessung; `fakten.py` Abschnitt 6).

5. **Fehlerdefinition (in Prozentpunkten, Pp):**
   - **Numerischer Fehler** (auf den **9.206** unzensierten Folgemessungen):
     $$e_{c,k}^{\text{num}} = \left|\hat{p}_{c,k} - p_{c,k}\right|$$
   - **Zensierter Fehler** (auf allen **10.363** Folgemessungen inkl. `'overfull'` $\ge 100\,\%$):
     $$e_{c,k}^{\text{zens}} = \begin{cases} \left|\hat{p}_{c,k} - p_{c,k}\right| & \text{falls Messung numerisch } (p_{c,k} \le 100) \\ \max\!\big(0,\; 100 - \hat{y}_{c,k}\big) & \text{falls Messung } \texttt{'overfull'} \; (y_{c,k} \ge 100) \end{cases}$$
     Sagt das Modell bei einer `'overfull'`-Messung $\hat{y}_{c,k} \ge 100\,\%$ voraus, ist die Bedingung $y_{c,k} \ge 100\,\%$ erfüllt und der Fehler beträgt $0\text{ Pp}$.

---

## 2. Benannte Annahmen (`AGENTS.md` Abschnitt 3)

| Kennung | Annahme | Auswirkung auf das Modell |
|---|---|---|
| **A1** | Jeder Besuch leert alle Kammern des Containers (`Location_id`) auf 0. | Auf Container-Ebene entsprechen die **4.468** Besuche **4.468** Leerungen (`fakten.py` Abschnitt 4). **Gesetzte Annahme, kein Befund:** streng A1 ergibt Median **9,7 Pp**, A4 **9,9 Pp** — innerhalb des Rauschens gleich (`fakten.py` Abschnitt 6). |
| **A2** | Füllrate je Kammer (`Location_id`, `material_type`) ist zwischen Besuchen konstant (Startwert, wird geprüft). | Lineares Wachstum $\hat{y}_{c,k} = r_c \cdot \Delta t_{c,k}$ mit einer festen Rate $r_c$ (`%/Tag`) je Kammer (`fakten.py` Abschnitt 6). |
| **A3** | `'overfull'` = Füllstand $\ge 100\,\%$, genauer Wert unbekannt. | Rechtszensierung: `'overfull'` (**1.192** Zeilen = **10,2 %**) geht nicht als `100` in den unzensierten Raten-Median ein, sondern als Untergrenze $r \ge 100 / \Delta t$ bzw. zensiertes Zielintervall $[100, \infty)$ (`fakten.py` Abschnitt 2 & 6). |
| **A4** | Jede Messung je `(Location_id, material_type)` ist zugleich eine Leerung dieser Kammer auf 0; das tägliche Wachstum (`% pro Tag`) bemisst sich aus dem Abstand zur letzten Messung derselben `(Location_id, material_type)`. | Vermeidet Verzerrungen durch die **1.407** Besuche, bei denen nur 1 (**296**) oder 2 (**1.111**) Farben gemessen wurden (`2.348` Folgemessungen mit `abstand_loc != abstand_farbe`; `fakten.py` Abschnitt 4 & 6). |
| **A5** | Gemessen wird **vor** der Leerung, geleert wird **nach** der Messung. | Die CSV enthält keinen Stand nach dem Besuch; die Leerung ist nur über die Folgemessung prüfbar. Beleg (`fakten.py` Abschnitt 9, $n = 8.328$ Paare mit numerischem Vorgängerstand): Start bei 0 ergibt **Median 9,5 Pp**, Wachstum ohne Leerung ab dem Vorgängerstand **24,4 Pp**; bei **40,7 %** der Paare liegt der nächste Stand niedriger als der vorherige. Die Leerung gewinnt. A5 sagt nur, **dass** geleert wird, nicht **welche** Kammern ein Besuch leert — dafür gilt A1. |

---

## 3. Geschätzte Füllraten und Bilanz-Fehler (`scripts/fakten.py` Abschnitt 6)

### 3.1 Verteilung der Füllraten je Container `(Location_id, material_type)`

| Kennzahl | Wert | Quelle (`fakten.py`) |
|---|---:|---|
| Container `(Location_id, material_type)` gesamt | **1.338** | Abschnitt 3 & 6 |
| – mit unzensierter Folgemessung (`r` aus `~ueber`) | **1.303** | Abschnitt 6 |
| – nur mit zensierter `'overfull'`-Folgemessung (Untergrenze $100/\Delta t$) | **1** | Abschnitt 6 |
| – ohne Folgemessung (nur 1 Messung im Zeitraum) | **34** | Abschnitt 6 |
| Füllrate `%/Tag` — **P10 / Median / P90** | **0,43 / 1,52 / 3,89 %/Tag** | Abschnitt 6 |
| Tage bis 100 % bei Median-Rate (Median über Container) | **65,9 Tage** | Abschnitt 6 |

### 3.2 Fehler beim Nachrechnen der Füllstände und Grenzwerte (`AGENTS.md` §4)

| Auswertung | Stichprobe $n$ | Median-Fehler | P90-Fehler | Mittlerer Fehler | Anteil $\le 10\text{ Pp}$ | Anteil $\le 20\text{ Pp}$ | Grenzwert (`AGENTS.md` §4) | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| **In-Sample numerisch** (`~ueber`) | **9.206** | **9,9 Pp** | **36,3 Pp** | **14,4 Pp** | **53,2 %** | **74,6 %** | Median $\le 10,0\text{ Pp}$, P90 $\le 37,0\text{ Pp}$, Mittel $\le 15,0\text{ Pp}$ | **Grün** |
| **In-Sample inkl. zensiert** (`'overfull'` $\ge 100\,\%$) | **10.363** | **8,9 Pp** | **36,4 Pp** | **13,9 Pp** | **55,1 %** | **75,2 %** | Median $\le 10,0\text{ Pp}$, P90 $\le 37,0\text{ Pp}$, Mittel $\le 15,0\text{ Pp}$ | **Grün** |
| **Backtest Out-of-Sample numerisch** (Train $\le$ `2026-04-09`, Test $>$ `2026-04-09`) | **5.239** | **15,1 Pp** | **48,1 Pp** | **20,4 Pp** | **38,7 %** | — | Median $\le 16,0\text{ Pp}$, P90 $\le 50,0\text{ Pp}$ | **Grün** |
| **Backtest Out-of-Sample inkl. zensiert** (Train $\le$ `2026-04-09`, Test $>$ `2026-04-09`) | **5.948** | **14,3 Pp** | **48,7 Pp** | **19,8 Pp** | **42,4 %** | — | Median $\le 16,0\text{ Pp}$, P90 $\le 50,0\text{ Pp}$ | **Grün** |

### 3.3 Überlaufquote im Modell vs. Daten (`AGENTS.md` §4 Punkt 3)

| Kennzahl | Daten (Ist) | Modell ($\hat{y} > 110\,\%$, nächste 10er-Stufe) | Modell ($\hat{y} \ge 100\,\%$) | Quelle (`fakten.py`) |
|---|---:|---:|---:|---|
| Anteil auf allen Folgemessungen ($n = 10.363$) | **11,2 %** | **13,7 %** | **19,9 %** | Abschnitt 6 |
| Anteil auf allen Messungen ($n = 11.701$) | **10,2 %** | **12,2 %** | **17,6 %** | Abschnitt 2 & 6 |
