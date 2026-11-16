"""Kalibrierungstest: reproduziert das Beobachtungsmodell der echten Daten in einer
Simulation und vergleicht simulierte mit echten Beobachtungen.

Simuliert wird der generative Prozess des Modells (src/modell.py): Rate je
(Location_id, material_type), linearer Zuwachs, Leerung auf 0 (A1/A4). Beobachtet
wird wie in der CSV (docs/grenzwerte.md Abschnitt 4, OBS-1..OBS-4, vorab fixiert):
- OBS-1: Stand auf nächste 10er-Stufe gerundet.
- OBS-2: Stand > 100 % -> 'overfull' (rechtszensiert, A3).
- OBS-3: gemessen wird nur bei echten Besuchen, echte Besuchsdaten, fehlende Farben
  wie in der CSV (simuliert werden genau die existierenden Mess-Zeilen).
- OBS-4: generative Rate = rate_fit (MAE-Fit je Container, src/modell.py); Zeilen
  ohne Rate / ohne Vorgänger fliegen raus.

Verglichen werden (Grenzwerte vorab in docs/grenzwerte.md §4 festgelegt):
- Overfull-Quote gesamt und je Farbe (|diff| <= 4.0 Pp),
- Quantile P10/P50/P90 der numerischen Füllstände (|diff| <= 10.0 Pp),
- Median je Abstands-Bucket <=7 / 8-14 / 15-30 / >30 Tage (|diff| <= 10.0 Pp).
Die KS-Statistik wird als Information mitberichtet (ohne Grenzwert).
Läuft der Test rot, bleibt er rot: kein Tuning, nur Bericht.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from domaene import DEFAULT_CSV, lade_messungen
from modell import schaetze_fuellraten

GRENZWERT_UEBER_PPA = 4.0
GRENZWERT_QUANTIL_PP = 10.0
GRENZWERT_BUCKET_PP = 10.0
FARBEN = ("brown", "green", "white")
BUCKETS = [("<=7", 0, 7), ("8-14", 8, 14), ("15-30", 15, 30), (">30", 31, 10**9)]
KS_INFO = {}  # Information ohne Grenzwert (docs/grenzwerte.md §4)


def _quantisiere(level: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """OBS-1/2: kontinuierlicher Stand -> (ueber, 10er-Stufe 0..100)."""
    ueber = level > 100.0
    stufe = np.minimum(np.floor(level / 10.0 + 0.5) * 10.0, 100.0)
    return ueber, stufe


def _ks_statistik(a: np.ndarray, b: np.ndarray) -> float:
    """Zwei-Stichproben-KS-Statistik (max |ECDF-Differenz|), nur Information."""
    x = np.sort(a)
    y = np.sort(b)
    alle = np.concatenate([x, y])
    cdf_x = np.searchsorted(x, alle, side="right") / len(x)
    cdf_y = np.searchsorted(y, alle, side="right") / len(y)
    return float(np.max(np.abs(cdf_x - cdf_y)))


@pytest.fixture(scope="module")
def vergleich() -> dict:
    """Baut die sim/echt-Vergleichstabelle (Folgemessungen, identisches Beobachtungsmodell)."""
    df = lade_messungen(DEFAULT_CSV)
    raten = schaetze_fuellraten(df)
    folge = df[df["abstand"] > 0].join(raten["rate_fit"], on=["Location_id", "material_type"])

    ohne_rate = int(folge["rate_fit"].isna().sum())
    folge = folge[folge["rate_fit"].notna()].copy()

    # Simulation (generativer Prozess) -> Beobachtungsmodell OBS-1/2
    sim_true = folge["rate_fit"] * folge["abstand"]
    sim_ueber, sim_stufe = _quantisiere(sim_true.values)
    folge["sim_ueber"] = sim_ueber
    folge["sim_p"] = np.where(sim_ueber, np.nan, sim_stufe)

    # Echt: gleiche Grundgesamtheit, gleiche Beobachtung (p ist NaN bei 'overfull')
    folge["echt_p"] = folge["p"]
    folge["echt_ueber"] = folge["ueber"]

    numerisch = folge[folge["sim_p"].notna() & folge["echt_p"].notna()]
    KS_INFO["ks_statistik"] = round(_ks_statistik(numerisch["echt_p"].values, numerisch["sim_p"].values), 4)
    KS_INFO["n_numerisch"] = int(len(numerisch))
    KS_INFO["n_ge_out_rate"] = ohne_rate

    return {"folge": folge, "numerisch": numerisch, "ohne_rate": ohne_rate}


def _ueber_quote(f: pd.DataFrame) -> tuple[float, float]:
    return float(f["echt_ueber"].mean() * 100), float(f["sim_ueber"].mean() * 100)


def test_overfull_quote_gesamt(vergleich: dict) -> None:
    echt, sim = _ueber_quote(vergleich["folge"])
    assert abs(echt - sim) <= GRENZWERT_UEBER_PPA, (
        f"Overfull-Quote gesamt: echt {echt:.1f} % vs. simuliert {sim:.1f} % "
        f"(|diff| {abs(echt - sim):.1f} Pp > {GRENZWERT_UEBER_PPA:.1f} Pp)"
    )


@pytest.mark.parametrize("farbe", FARBEN)
def test_overfull_quote_je_farbe(vergleich: dict, farbe: str) -> None:
    echt, sim = _ueber_quote(vergleich["folge"][vergleich["folge"]["material_type"] == farbe])
    assert abs(echt - sim) <= GRENZWERT_UEBER_PPA, (
        f"Overfull-Quote {farbe}: echt {echt:.1f} % vs. simuliert {sim:.1f} % "
        f"(|diff| {abs(echt - sim):.1f} Pp > {GRENZWERT_UEBER_PPA:.1f} Pp)"
    )


@pytest.mark.parametrize("q", [10, 50, 90])
def test_quantile_numerisch(vergleich: dict, q: int) -> None:
    echt = float(vergleich["numerisch"]["echt_p"].quantile(q / 100))
    sim = float(vergleich["numerisch"]["sim_p"].quantile(q / 100))
    assert abs(echt - sim) <= GRENZWERT_QUANTIL_PP, (
        f"P{q} der Füllstände: echt {echt:.0f} % vs. simuliert {sim:.0f} % "
        f"(|diff| {abs(echt - sim):.1f} Pp > {GRENZWERT_QUANTIL_PP:.1f} Pp)"
    )


@pytest.mark.parametrize("label", [b[0] for b in BUCKETS])
def test_median_je_abstandsbucket(vergleich: dict, label: str) -> None:
    _, lo, hi = next(b for b in BUCKETS if b[0] == label)
    folge = vergleich["folge"]
    auswahl = (folge["abstand"] >= lo) & (folge["abstand"] <= hi)
    echt = float(folge.loc[auswahl, "echt_p"].median())
    sim = float(folge.loc[auswahl, "sim_p"].median())
    assert abs(echt - sim) <= GRENZWERT_BUCKET_PP, (
        f"Median Füllstand im Bucket {label} Tage: echt {echt:.0f} % vs. simuliert {sim:.0f} % "
        f"(|diff| {abs(echt - sim):.1f} Pp > {GRENZWERT_BUCKET_PP:.1f} Pp)"
    )


def test_bericht_ablegen(vergleich: dict) -> None:
    """Legt alle Ist-Zahlen als JSON ab (Berichtsquelle, deterministisch)."""
    folge, numerisch = vergleich["folge"], vergleich["numerisch"]
    bericht: dict = {
        "grenzwerte": {"ueber_ppa": GRENZWERT_UEBER_PPA, "quantil_pp": GRENZWERT_QUANTIL_PP, "bucket_pp": GRENZWERT_BUCKET_PP},
        "n_folge": int(len(folge)),
        "n_numerisch": int(len(numerisch)),
        "ohne_rate_ge_out": vergleich["ohne_rate"],
        "ks_statistik": KS_INFO.get("ks_statistik"),
        "ueber_quote": {"gesamt": dict(zip(("echt", "sim"), _ueber_quote(folge)))},
        "ueber_quote_je_farbe": {
            f: dict(zip(("echt", "sim"), _ueber_quote(folge[folge["material_type"] == f])))
            for f in FARBEN
        },
        "quantile_numerisch": {
            f"P{q}": {
                "echt": float(numerisch["echt_p"].quantile(q / 100)),
                "sim": float(numerisch["sim_p"].quantile(q / 100)),
            }
            for q in (10, 50, 90)
        },
        "median_bucket": {},
    }
    for label, lo, hi in BUCKETS:
        auswahl = (folge["abstand"] >= lo) & (folge["abstand"] <= hi)
        bericht["median_bucket"][label] = {
            "echt": float(folge.loc[auswahl, "echt_p"].median()),
            "sim": float(folge.loc[auswahl, "sim_p"].median()),
            "n": int(auswahl.sum()),
        }
    out = ROOT / "data" / "derived" / "kalibrierung.json"
    out.write_text(json.dumps(bericht, indent=2, ensure_ascii=False), encoding="utf-8")
