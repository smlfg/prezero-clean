"""Kalibrierungsbericht: bestehendes Modell gegen echte Beobachtungen.

Die Grenzwerte in diesem Test stehen absichtlich vor der Berechnung fest. Der Test
simuliert ausschließlich auf dem echten Besuchsplan: gemessen werden nur die Farben,
die in der CSV vorkommen; ``overfull`` ist rechtszensiert wie in den Rohdaten.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path: sys.path.insert(0, str(ROOT / "src"))
from modell import DEFAULT_CSV, lade_messungen, schaetze_fuellraten, simuliere_beobachtungsmodell  # noqa: E402
MAX_UEBERFULL_DIFF = 0.02
MAX_UEBERFULL_COLOR_DIFF = 0.03
MAX_QUANTIL_DIFF_PP = 10.0
MAX_BUCKET_MEDIAN_DIFF_PP = 10.0

def _vorbereiten() -> pd.DataFrame:
    df = lade_messungen(DEFAULT_CSV)
    sim = simuliere_beobachtungsmodell(df, schaetze_fuellraten(df))
    sim["real_p_untergrenze"] = sim["p_untergrenze"]
    sim["bucket"] = pd.cut(sim["abstand"], bins=[0, 7, 14, 30, np.inf], labels=["≤7", "8–14", "15–30", ">30"])
    return sim[sim["abstand"] > 0].copy()

def _status(ok: bool) -> str:
    return "GRÜN" if ok else "ROT"

def test_kalibrierung_beobachtungsmodell_berichten():
    sim = _vorbereiten()
    gesamt_real = float(sim["ueber"].mean())
    gesamt_sim = float(sim["sim_fill_level_perc"].eq("overfull").mean())
    print(f"\nKalibrierung Überfull gesamt: real={gesamt_real:.1%}, sim={gesamt_sim:.1%}, Grenze ±{MAX_UEBERFULL_DIFF:.1%}, Status={_status(abs(gesamt_sim-gesamt_real) <= MAX_UEBERFULL_DIFF)}")
    for farbe, gruppe in sim.groupby("material_type"):
        real = float(gruppe["ueber"].mean()); modell = float(gruppe["sim_fill_level_perc"].eq("overfull").mean())
        print(f"Kalibrierung Überfull {farbe}: real={real:.1%}, sim={modell:.1%}, Grenze ±{MAX_UEBERFULL_COLOR_DIFF:.1%}, Status={_status(abs(modell-real) <= MAX_UEBERFULL_COLOR_DIFF)}")
    for quantil in (0.1, 0.5, 0.9):
        real = float(sim["real_p_untergrenze"].quantile(quantil)); modell = float(sim["sim_p_untergrenze"].quantile(quantil))
        print(f"Kalibrierung Quantil P{quantil:.0%}: real={real:.1f}, sim={modell:.1f}, Grenze ±{MAX_QUANTIL_DIFF_PP:.1f} Pp, Status={_status(abs(modell-real) <= MAX_QUANTIL_DIFF_PP)}")
    for bucket, gruppe in sim.groupby("bucket", observed=True):
        real = float(gruppe["real_p_untergrenze"].median()); modell = float(gruppe["sim_p_untergrenze"].median())
        print(f"Kalibrierung Abstand {bucket}: real Median={real:.1f}, sim Median={modell:.1f}, Grenze ±{MAX_BUCKET_MEDIAN_DIFF_PP:.1f} Pp, Status={_status(abs(modell-real) <= MAX_BUCKET_MEDIAN_DIFF_PP)}")
    assert len(sim) > 0
    assert set(sim["bucket"].dropna().unique()) <= {"≤7", "8–14", "15–30", ">30"}
    assert sim["sim_fill_level_perc"].eq("overfull").equals(sim["pred_raw"] >= 100.0)
