"""Bilanztest-Gate gemäß AGENTS.md §4.

Prüft das Puffer-Modell (src/modell.py) gegen die realen Füllstandsdaten:
1. Besuche = Leerungen im Modell (Anzahl identisch zur CSV: 4.468 Besuche, 11.701 Messungen).
2. Rate * Abstand reproduziert den gemessenen Stand innerhalb des Grenzwerts in AGENTS.md
   (meldet Fehler in Prozentpunkten: Median, P90, Mittelwert; bricht rot ab bei Überschreitung).
3. Behandelt 'overfull' als rechtszensierten Wert (>= 100 %), nicht als 100, und erzeugt
   'overfull' ungefähr so oft wie die Daten (10,2 % gesamt / 11,2 % auf Folgemessungen).
4. Backtest ohne Blick in die Zukunft (Training <= 2026-04-09, Test > 2026-04-09).
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

from modell import (
    DEFAULT_CSV,
    GRENZWERT_MAE_PP,
    GRENZWERT_MEDIAN_PP,
    GRENZWERT_OOS_MEDIAN_PP,
    GRENZWERT_OOS_P90_PP,
    GRENZWERT_P90_PP,
    UEBERLAUF_TOLERANZ_PP,
    backtest_zeitlich,
    bilanz_kennzahlen,
    lade_messungen,
    schaetze_fuellraten,
    simuliere_puffer,
)


def test_1_besuche_und_messungen_gleich_leerungen():
    """1. Besuche = Leerungen im Modell (Anzahl exakt identisch zur CSV)."""
    df = lade_messungen(DEFAULT_CSV)
    sim = simuliere_puffer(df)
    kz = bilanz_kennzahlen(sim)

    raw = pd.read_csv(DEFAULT_CSV)
    besuche_csv = int(raw.groupby(["Location_id", "date"]).ngroups)
    messungen_csv = len(raw)

    assert besuche_csv == 4468
    assert messungen_csv == 11701
    assert kz["leerungen_standort"] == besuche_csv
    assert kz["leerungen_container"] == messungen_csv
    assert (sim["stand_nach_leerung"] == 0.0).all()


def test_2_fuellstand_nachrechnen_median_und_p90():
    """2. Modell rechnet Füllstände nach; meldet Median & P90 (Pp) und prüft Grenzwerte."""
    df = lade_messungen(DEFAULT_CSV)
    raten = schaetze_fuellraten(df)
    sim = simuliere_puffer(df, raten)
    kz = bilanz_kennzahlen(sim)

    median_pp = kz["fehler_median_pp"]
    p90_pp = kz["fehler_p90_pp"]
    mittel_pp = kz["fehler_mittel_pp"]
    zens_median_pp = kz["fehler_zensiert_median_pp"]
    zens_p90_pp = kz["fehler_zensiert_p90_pp"]

    print(
        f"\n[Bilanztest In-Sample numerisch (n={kz['folgemessungen_numerisch']})] "
        f"Median: {median_pp:.1f} Pp | P90: {p90_pp:.1f} Pp | Mittel: {mittel_pp:.1f} Pp"
    )
    print(
        f"[Bilanztest In-Sample inkl. zensiert (n={kz['folgemessungen_gesamt']})] "
        f"Median: {zens_median_pp:.1f} Pp | P90: {zens_p90_pp:.1f} Pp"
    )

    assert median_pp <= GRENZWERT_MEDIAN_PP, (
        f"In-Sample Median-Fehler {median_pp:.1f} Pp > Grenzwert {GRENZWERT_MEDIAN_PP:.1f} Pp"
    )
    assert p90_pp <= GRENZWERT_P90_PP, (
        f"In-Sample P90-Fehler {p90_pp:.1f} Pp > Grenzwert {GRENZWERT_P90_PP:.1f} Pp"
    )
    assert mittel_pp <= GRENZWERT_MAE_PP, (
        f"In-Sample mittlerer Fehler {mittel_pp:.1f} Pp > Grenzwert {GRENZWERT_MAE_PP:.1f} Pp"
    )
    assert zens_median_pp <= GRENZWERT_MEDIAN_PP, (
        f"Zensierter Median-Fehler {zens_median_pp:.1f} Pp > Grenzwert {GRENZWERT_MEDIAN_PP:.1f} Pp"
    )
    assert zens_p90_pp <= GRENZWERT_P90_PP, (
        f"Zensierter P90-Fehler {zens_p90_pp:.1f} Pp > Grenzwert {GRENZWERT_P90_PP:.1f} Pp"
    )


def test_3_overfull_zensiert_und_ueberlaufquote():
    """3. 'overfull' wird als zensierter Wert (>= 100 %) behandelt, nicht als 100."""
    df = lade_messungen(DEFAULT_CSV)
    raten = schaetze_fuellraten(df)
    sim = simuliere_puffer(df, raten)
    kz = bilanz_kennzahlen(sim)

    # 'overfull' hat in Spalte p den Wert NaN (nicht 100) und Untergrenze 100.0
    assert int(df["ueber"].sum()) == 1192
    assert df.loc[df["ueber"], "p"].isna().all()
    assert (df.loc[df["ueber"], "p_untergrenze"] == 100.0).all()

    # Bei zensierten 'overfull'-Zeilen mit Vorhersage >= 100 % ist der zensierte Fehler exakt 0 Pp
    ueber_hoch = sim["ueber"] & (sim["pred_raw"] >= 100.0)
    assert int(ueber_hoch.sum()) > 0
    assert (sim.loc[ueber_hoch, "fehler_zensiert"] == 0.0).all()

    # Naive Behandlung (overfull = 100) würde die geschätzten Raten nach unten verzerren
    folge = df[df["abstand"] > 0].copy()
    folge["rate_naiv_100"] = folge["p"].fillna(100.0) / folge["abstand"]
    r_naiv = folge.groupby(["Location_id", "material_type"])["rate_naiv_100"].median()
    assert float(raten["rate_unzensiert_med"].median()) > float(r_naiv.median())

    # Überlaufquote im Modell nahe an den Daten (11,2 % auf Folgemessungen, Toleranz +-4 Pp)
    diff_quote = abs(kz["ueberlauf_quote_modell_folge"] - kz["ueberlauf_quote_daten_folge"])
    assert diff_quote <= UEBERLAUF_TOLERANZ_PP, (
        f"Modell-Überlaufquote {kz['ueberlauf_quote_modell_folge']:.1%} weicht um "
        f"{diff_quote:.1%} von Daten {kz['ueberlauf_quote_daten_folge']:.1%} ab"
    )


def test_4_backtest_ohne_zukunftsblick():
    """4. Chronologischer Backtest (Training <= 2026-04-09, Test > 2026-04-09)."""
    df = lade_messungen(DEFAULT_CSV)
    bt = backtest_zeitlich(df)

    print(
        f"\n[Bilanztest Backtest > {bt['stichtag']} (n={bt['n_test_numerisch']})] "
        f"Median: {bt['oos_fehler_median_pp']:.1f} Pp | P90: {bt['oos_fehler_p90_pp']:.1f} Pp"
    )

    assert bt["oos_fehler_median_pp"] <= GRENZWERT_OOS_MEDIAN_PP, (
        f"Out-of-Sample Median-Fehler {bt['oos_fehler_median_pp']:.1f} Pp > "
        f"Grenzwert {GRENZWERT_OOS_MEDIAN_PP:.1f} Pp"
    )
    assert bt["oos_fehler_p90_pp"] <= GRENZWERT_OOS_P90_PP, (
        f"Out-of-Sample P90-Fehler {bt['oos_fehler_p90_pp']:.1f} Pp > "
        f"Grenzwert {GRENZWERT_OOS_P90_PP:.1f} Pp"
    )
    assert bt["oos_zensiert_median_pp"] <= GRENZWERT_OOS_MEDIAN_PP
    assert bt["oos_zensiert_p90_pp"] <= GRENZWERT_OOS_P90_PP
