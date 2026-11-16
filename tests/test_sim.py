"""Tests der Simulation (docs/KINO_VERTRAG.md).

Geprueft wird die Python-Referenz (scripts/sim_referenz.py). Die JavaScript-Engine
(sim/engine.js) wird separat gegen diese Referenz verglichen: scripts/sim_vergleich.py.
"""
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from sim_referenz import run, lade  # noqa: E402

BESUCHE_CSV = 4468
TAGE = 348
N_ORT = 449


@pytest.fixture(scope="module")
def daten():
    return lade()


def test_1_determinismus(daten):
    """Zwei Laeufe mit gleichen Parametern liefern gleiche Zahlen."""
    a = run(5, 1, "ist", 80, daten=daten)
    b = run(5, 1, "ist", 80, daten=daten)
    for key in ("leerungen", "ueberlauf_tage", "voll_bei_leerung_pct",
                "ueber_100_bei_leerung_pct", "mittel_max_bei_leerung_pct",
                "fuell_mittel", "auslastung_pct"):
        assert a[key] == b[key], key


def test_2_ist_rhythmus_reproduziert_die_beobachteten_besuche(daten):
    """Der kalibrierte Ist-Rhythmus verlangt die beobachteten 4.468 Besuche."""
    m = run(5, 1, "ist", 80, daten=daten)
    abweichung = abs(m["leerungen"] - BESUCHE_CSV) / BESUCHE_CSV
    assert abweichung < 0.05, (
        f"{m['leerungen']} Leerungen statt {BESUCHE_CSV} Besuche "
        f"({abweichung:.1%} Abweichung)")


def test_3_abstand_haelt_die_stops_pro_tag_und_der_sollwert(daten):
    """Doppelter Abstand -> halbe Stopps/Tag (Soll und tatsaechlich)."""
    klein = run(5, 1, "ist", 80, daten=daten)
    gross = run(10, 1, "ist", 80, daten=daten)
    assert klein["soll_stopps_pro_tag"] == pytest.approx(12.8, abs=0.05)
    assert gross["soll_stopps_pro_tag"] == pytest.approx(6.4, abs=0.05)
    verhaeltnis = gross["stopps_pro_tag"] / klein["stopps_pro_tag"]
    assert 0.45 <= verhaeltnis <= 0.55, verhaeltnis


def test_4_mehr_autos_helfen_beim_rueckstau(daten):
    """Bei Rueckstau (Strategie nach Fuellstand) senken mehr Autos den Ueberlauf."""
    eins = run(5, 1, "fuell", 80, daten=daten)
    vier = run(5, 4, "fuell", 80, daten=daten)
    assert vier["ueberlauf_tage"] <= eins["ueberlauf_tage"]
    assert vier["leerungen"] >= eins["leerungen"]


def test_5_plausibilitaet_default(daten):
    """Der Default-Lauf ist weder leer noch komplett ueberlaufen."""
    m = run(5, 1, "ist", 80, daten=daten)
    assert m["leerungen"] > 0
    assert 0 < m["ueberlauf_tage"] < N_ORT * TAGE
    assert 0 <= m["fuell_mittel"] <= 100
    assert m["auslastung_pct"] <= 100.5


def test_6_grosse_abstaende_machen_alles_uebervoll(daten):
    """Bei s=20 reicht die Kapazitaet nicht mehr: jeder Stopp trifft einen vollen Container."""
    m = run(20, 1, "ist", 80, daten=daten)
    assert m["voll_bei_leerung_pct"] == 100.0
    assert m["stopps_pro_tag"] < run(5, 1, "ist", 80, daten=daten)["stopps_pro_tag"]


def test_7_producer_consumer_bilanz(daten):
    """Produziert (Summe der Raten) und abgeholt (Summe der Staende bei Leerung).

    Der Lauf startet leer, deshalb kann er nie mehr abholen als erzeugt wurde:
    abgeholt = produziert - Bestand, und der Bestand ist nie negativ.
    """
    m = run(5, 1, "ist", 80, daten=daten)
    assert m["produziert_pp_pro_tag"] == pytest.approx(
        daten["meta"]["produziert_pp_pro_tag"], abs=0.01)
    assert m["abgeholt_pp"] <= m["produziert_pp"] + 1.0
    assert m["abgeholt_pp"] > 0.5 * m["produziert_pp"]
    assert m["bilanz_pp"] == pytest.approx(m["produziert_pp"] - m["abgeholt_pp"], abs=0.2)
