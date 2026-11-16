"""Gate für das Domänenmodell `Glas` – `Container` – `LKW` (AGENTS.md §2).

Prüft, dass die drei Objekte in `src/domaene.py` die CSV unverändert abbilden:

1. Mengengerüst: Container, Kammern, Messungen, Besuche stimmen mit der CSV überein.
2. **Messen und Leeren sind zwei Mengen**: bei 1.393 Besuchen wurde nur eine
   Teilmenge der Kammern gemessen (AGENTS.md §2), während A1 alle Kammern leert.
3. `Glas`/`Container`/`LKW` verhalten sich wie im Modell: Füllstand vor der
   Leerung (A5), `overfull` rechtszensiert (A3), Leeren setzt alle Kammern auf 0.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from domaene import (
    FARBEN,
    LKW,
    Container,
    Glas,
    Kammer,
    baue_besuche,
    baue_container,
    domaene_kennzahlen,
    lade_messungen,
)


def test_1_mengengeruest_stimmt_mit_csv():
    """1. Container, Kammern, Messungen und Besuche == CSV."""
    df = lade_messungen()
    kz = domaene_kennzahlen(df)

    raw = pd.read_csv(
        ROOT / "data" / "raw" / "glass_fill_levels_anonymized_f.csv", parse_dates=["date"]
    )
    assert kz["container"] == raw["Location_id"].nunique() == 449
    assert kz["kammern"] == raw.groupby(["Location_id", "material_type"]).ngroups == 1338
    assert kz["messungen"] == len(raw) == 11701
    assert kz["besuche"] == raw.groupby(["Location_id", "date"]).ngroups == 4468
    assert kz["ueberlauf_messungen"] == 1192

    # Kammern je Container: 441 mit drei Farben, 7 mit zwei, 1 mit einer.
    assert kz["kammern_je_container"] == {1: 1, 2: 7, 3: 441}


def test_2_messen_und_leeren_sind_zwei_mengen():
    """2. Ein Besuch kann alle Kammern leeren und trotzdem nur eine messen."""
    df = lade_messungen()
    kz = domaene_kennzahlen(df)
    assert kz["besuche_messen_teilmenge"] == 1393
    assert kz["besuche_messen_alle_kammern"] == 3075
    assert kz["besuche_messen_alle_kammern"] + kz["besuche_messen_teilmenge"] == kz["besuche"]

    besuche = baue_besuche(df)
    assert len(besuche) == kz["besuche"]

    # A1: jeder Besuch leert alle Kammern des Containers (auch die ungemessenen).
    kammern_je_id = df.groupby("Location_id")["material_type"].nunique()
    for b in besuche:
        assert len(b.geleert) == kammern_je_id[b.location_id]
        assert b.gemessen <= b.geleert

    # Es gibt Besuche, die nur eine Teilmenge messen (Farbe fehlt in der Messung).
    teilmessungen = [b for b in besuche if len(b.gemessen) < len(b.geleert)]
    assert len(teilmessungen) == 1393


def test_3_glas_container_lkw_verhalten():
    """3. Glas/Container/LKW: A3 (overfull), A5 (vor der Leerung), A1 (leert alle)."""
    # A3: 'overfull' erst oberhalb von 100 %, rechtszensiert.
    assert Glas("white", 100.0).ablesen() == 100.0
    assert Glas("white", 100.1).ablesen() == "overfull"
    assert Glas("white", 120.0).uebervoll is True

    # A5: gemessen wird vor der Leerung.
    container = Container.aus_messungen("L1", ["brown", "green", "white"])
    container.kammern["brown"].fuellstand = 40.0
    container.kammern["green"].fuellstand = 100.0
    container.kammern["white"].fuellstand = 120.0

    lkw = LKW()
    besuch = lkw.besuchen(container, pd.Timestamp("2026-01-01"))

    assert besuch.gemessen == frozenset({"brown", "green", "white"})
    assert besuch.geleert == frozenset({"brown", "green", "white"})
    # Der Messwert ist der Stand VOR der Leerung.
    assert container.kammern["brown"].fuellstand == 0.0
    assert container.kammern["green"].fuellstand == 0.0

    # A1: auch ungemessene Kammern werden geleert.
    container2 = Container.aus_messungen("L2", ["brown", "green", "white"])
    container2.kammern["green"].fuellstand = 70.0
    lkw2 = LKW()
    b2 = lkw2.besuchen(container2, pd.Timestamp("2026-01-02"))
    assert b2.gemessen == frozenset({"brown", "green", "white"})
    assert container2.kammern["green"].fuellstand == 0.0


def test_4_container_und_besuche_aus_den_daten():
    """4. Container und Besuche lassen sich vollständig aus der CSV bauen."""
    df = lade_messungen()
    container = baue_container(df)
    assert len(container) == 449
    assert sum(len(c.kammern) for c in container.values()) == 1338
    assert all(set(c.kammern) <= set(FARBEN) for c in container.values())
    assert all(isinstance(k, Kammer) for c in container.values() for k in c.kammern.values())

    besuche = baue_besuche(df)
    assert len({(b.location_id, b.datum) for b in besuche}) == 4468
    assert all(b.datum.tz is None for b in besuche)


def test_5_messwerte_rundlauf_unveraendert():
    """5. Alle 11.701 Messwerte laufen unverändert durch das Modell.

    Der CSV-Wert ist der Füllstand **vor** der Leerung (A5). Wird die Kammer auf
    diesen Stand gesetzt und danach abgelesen, muss exakt der CSV-Wert zurückkommen
    — auch für die 1.192 rechtszensierten 'overfull'-Werte (A3).
    """
    df = lade_messungen()
    container = baue_container(df)

    geprueft = 0
    for (lid, _datum), sub in df.groupby(["Location_id", "date"], sort=True):
        c = container[lid]
        for _, row in sub.iterrows():
            # Stand setzen; bei 'overfull' ist der wahre Wert >= 100 % (zensiert, A3).
            c.kammern[row["material_type"]].fuellstand = (
                120.0 if row["ueber"] else float(row["p"])
            )
            abgelesen = c.messen()[row["material_type"]]
            if row["ueber"]:
                assert abgelesen == "overfull"
            else:
                assert float(abgelesen) == float(row["p"])
            geprueft += 1
        c.leeren()  # A1: alle Kammern auf 0

    assert geprueft == 11701

    # Nach dem letzten Besuch steht jede Kammer auf 0 (A1).
    assert all(
        k.fuellstand == 0.0 for c in container.values() for k in c.kammern.values()
    )
