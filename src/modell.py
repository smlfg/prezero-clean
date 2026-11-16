"""Puffer-Modell je Container (Location_id, material_type).

Grundlage: docs/datenmodell.md, AGENTS.md (Annahmen A1-A4), scripts/fakten.py (Abschnitt 5 & 6).
Erlaubte Spalten: Location_id, material_type, date, fill_level_perc.

Modellgleichung je Container c = (Location_id, material_type):
- Abfluss (Leerung): Jede Messung (Location_id, material_type, date) leert den Puffer auf 0 % (A1, A4).
- Zufluss (Füllrate): Zwischen zwei Messungen mit Abstand dt (in Tagen) wächst der Stand
  linear mit konstanter täglicher Rate r_c (% pro Tag Wachstum, A2):
      y_hat = r_c * dt
      p_hat = min(r_c * dt, 100)
- Zensierung ('overfull', A3): 'overfull' ist rechtszensiert (wahrer Stand >= 100 %), nicht 100.
  In der Ratenschätzung wird 'overfull' nicht als 100 eingesetzt, sondern liefert die
  untere Schranke r_min = 100 / dt. Beim Nachrechnen ist der zensierte Fehler
  max(0, 100 - y_hat) (0 Pp, sobald y_hat >= 100 %).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "raw" / "glass_fill_levels_anonymized_f.csv"
ERLAUBTE_SPALTEN = ["Location_id", "material_type", "date", "fill_level_perc"]

# Grenzwerte gemäß AGENTS.md §4 (von Samuel festgelegt)
GRENZWERT_MEDIAN_PP = 10.0
GRENZWERT_P90_PP = 37.0
GRENZWERT_MAE_PP = 15.0
GRENZWERT_OOS_MEDIAN_PP = 16.0
GRENZWERT_OOS_P90_PP = 50.0
UEBERLAUF_TOLERANZ_PP = 0.04


def lade_messungen(csv_pfad: str | Path = DEFAULT_CSV) -> pd.DataFrame:
    """Lädt die Rohdaten (nur die 4 erlaubten Spalten) und berechnet Besuchsabstände.

    - Behandelt 'overfull' als rechtszensierten Wert (>= 100 %), nicht als 100:
      Spalte `p` ist für 'overfull' NaN, Spalte `p_untergrenze` ist 100.0.
    - Berechnet `abstand` in Tagen zur vorigen Messung derselben (Location_id, material_type) (A4)
      sowie `abstand_ort` zum vorigen Standort-Besuch (Location_id, date) (A1).
    """
    raw = pd.read_csv(csv_pfad, usecols=ERLAUBTE_SPALTEN, parse_dates=["date"])
    d = raw[ERLAUBTE_SPALTEN].copy()
    d["ueber"] = d["fill_level_perc"].eq("overfull")
    d["p"] = pd.to_numeric(d["fill_level_perc"].where(~d["ueber"]))
    d["p_untergrenze"] = np.where(d["ueber"], 100.0, d["p"])

    # Standort-Besuchsabstand (Location_id, date)
    v = d[["Location_id", "date"]].drop_duplicates().sort_values(["Location_id", "date"])
    v["abstand_ort"] = v.groupby("Location_id")["date"].diff().dt.days
    d = d.merge(v, on=["Location_id", "date"], how="left")

    # Container-Messabstand (Location_id, material_type) -> nach jeder Messung Leerung auf 0 %
    d = d.sort_values(["Location_id", "material_type", "date"]).reset_index(drop=True)
    d["abstand"] = d.groupby(["Location_id", "material_type"])["date"].diff().dt.days

    # Tägliches Wachstum (% pro Tag) auf unzensierten Intervallen; Untergrenze auf 'overfull'
    folge = d["abstand"] > 0
    d["rate_unzensiert"] = np.where(folge & ~d["ueber"], d["p"] / d["abstand"], np.nan)
    d["rate_min_zensiert"] = np.where(folge & d["ueber"], 100.0 / d["abstand"], np.nan)
    return d


def schaetze_fuellraten(df: pd.DataFrame) -> pd.DataFrame:
    """Schätzt die Füllrate (% pro Tag) je Container (Location_id, material_type).

    - Unzensierte Intervalle (~ueber & abstand > 0): r_k = p_k / abstand_k -> Median je Container.
    - Zensierte Intervalle (ueber & abstand > 0): 'overfull' wird NICHT als 100 in den
      unzensierten Median gemischt, sondern liefert die Untergrenze r_min = 100 / abstand_k.
      Hat ein Container ausschließlich 'overfull'-Folgemessungen, wird diese Untergrenze
      als Mindestrate (rate_med) verwendet.
    """
    grp = df.groupby(["Location_id", "material_type"])
    basis = grp.agg(
        messungen=("date", "size"),
        folgemessungen=("abstand", lambda s: int((s > 0).sum())),
        n_unzensiert=("rate_unzensiert", lambda s: int(s.notna().sum())),
        n_ueberlauf=("rate_min_zensiert", lambda s: int(s.notna().sum())),
        rate_unzensiert_med=("rate_unzensiert", "median"),
        rate_zensiert_min_med=("rate_min_zensiert", "median"),
    )
    basis["rate_med"] = basis["rate_unzensiert_med"].combine_first(basis["rate_zensiert_min_med"])
    basis["tage_bis_100"] = 100.0 / basis["rate_med"].where(basis["rate_med"] > 0)
    return basis


def simuliere_puffer(
    df: pd.DataFrame, raten: pd.DataFrame | pd.Series | None = None
) -> pd.DataFrame:
    """Rechnet den Puffer je (Location_id, material_type) nach.

    - Abfluss: Nach jeder Messung startet der Puffer bei 0 % (`stand_nach_leerung = 0.0`).
    - Zufluss: Bis zur nächsten Messung nach `abstand` Tagen fließt `pred_raw = rate_med * abstand` zu.
    - Gedeckelter Skalenwert: `pred = min(pred_raw, 100.0)`.
    - Fehler (Prozentpunkte):
      * `fehler_numerisch`: |pred - p| auf unzensierten Folgemessungen (~ueber & abstand > 0).
      * `fehler_zensiert`: |pred - p| für numerische Messungen, und max(0, 100 - pred_raw)
        für rechtszensierte 'overfull'-Messungen (wahrer Wert >= 100 %).
    """
    if raten is None:
        raten_df = schaetze_fuellraten(df)
        rate_ser = raten_df["rate_med"].rename("rate_med")
    elif isinstance(raten, pd.DataFrame):
        rate_ser = raten["rate_med"].rename("rate_med")
    else:
        rate_ser = raten.rename("rate_med")

    sim = df.join(rate_ser, on=["Location_id", "material_type"]).copy()
    sim["stand_nach_leerung"] = 0.0
    sim["pred_raw"] = sim["rate_med"] * sim["abstand"]
    sim["pred"] = sim["pred_raw"].clip(upper=100.0)
    sim["pred_ab_100"] = sim["pred_raw"] >= 100.0
    sim["pred_ueber_100"] = sim["pred_raw"] > 100.0
    sim["pred_ueber"] = sim["pred_raw"] > 110.0

    ist_folge = (sim["abstand"] > 0) & sim["rate_med"].notna()
    sim["fehler_numerisch"] = np.where(
        ist_folge & ~sim["ueber"], (sim["pred"] - sim["p"]).abs(), np.nan
    )
    sim["fehler_zensiert"] = np.where(
        ~ist_folge,
        np.nan,
        np.where(
            ~sim["ueber"],
            (sim["pred"] - sim["p"]).abs(),
            np.maximum(0.0, 100.0 - sim["pred_raw"]),
        ),
    )
    return sim


def bilanz_kennzahlen(sim: pd.DataFrame) -> dict[str, float | int]:
    """Berechnet die Bilanz- und Fehlerkennzahlen (Median, P90, Mittelwert, Überlaufquote)."""
    f_num = sim["fehler_numerisch"].dropna()
    f_zens = sim["fehler_zensiert"].dropna()
    folge = sim[sim["abstand"] > 0]

    return {
        "messungen_gesamt": len(sim),
        "besuche_gesamt": int(sim.groupby(["Location_id", "date"]).ngroups),
        "leerungen_container": len(sim),
        "leerungen_standort": int(sim.groupby(["Location_id", "date"]).ngroups),
        "container_gesamt": int(sim.groupby(["Location_id", "material_type"]).ngroups),
        "folgemessungen_gesamt": len(folge),
        "folgemessungen_numerisch": len(f_num),
        "folgemessungen_overfull": int(folge["ueber"].sum()),
        "fehler_median_pp": float(f_num.median()),
        "fehler_p90_pp": float(f_num.quantile(0.9)),
        "fehler_mittel_pp": float(f_num.mean()),
        "anteil_bis_10_pp": float((f_num <= 10.0).mean()),
        "anteil_bis_20_pp": float((f_num <= 20.0).mean()),
        "fehler_zensiert_median_pp": float(f_zens.median()),
        "fehler_zensiert_p90_pp": float(f_zens.quantile(0.9)),
        "fehler_zensiert_mittel_pp": float(f_zens.mean()),
        "anteil_zensiert_bis_10_pp": float((f_zens <= 10.0).mean()),
        "anteil_zensiert_bis_20_pp": float((f_zens <= 20.0).mean()),
        "ueberlauf_quote_daten_gesamt": float(sim["ueber"].mean()),
        "ueberlauf_quote_daten_folge": float(folge["ueber"].mean()),
        "ueberlauf_quote_modell_folge": float(folge["pred_ueber"].mean()),
        "ueberlauf_quote_modell_ab_100_folge": float(folge["pred_ab_100"].mean()),
    }


def backtest_zeitlich(
    df: pd.DataFrame, stichtag: str | pd.Timestamp | None = None
) -> dict[str, float | int | str]:
    """Chronologischer Backtest ohne Blick in die Zukunft (Training <= Stichtag, Test > Stichtag)."""
    if stichtag is None:
        stichtag_ts = df["date"].min() + (df["date"].max() - df["date"].min()) / 2
    else:
        stichtag_ts = pd.Timestamp(stichtag)

    folge = df[df["abstand"] > 0].copy()
    train_folge = folge[folge["date"] <= stichtag_ts]
    test_folge = folge[folge["date"] > stichtag_ts].copy()

    # Schätze Raten ausschließlich auf den Trainings-Folgemessungen
    r_tr_unc = train_folge.groupby(["Location_id", "material_type"])["rate_unzensiert"].median()
    r_tr_ov = train_folge.groupby(["Location_id", "material_type"])["rate_min_zensiert"].median()
    r_tr_full = r_tr_unc.combine_first(r_tr_ov).rename("rate_med")

    # 1. Numerische Auswertung (exakt wie scripts/fakten.py Abschnitt 6)
    te_num = test_folge[~test_folge["ueber"]].join(
        r_tr_unc.rename("rate_tr"), on=["Location_id", "material_type"]
    ).dropna(subset=["rate_tr"])
    f_oos_num = ((te_num["rate_tr"] * te_num["abstand"]).clip(upper=100.0) - te_num["p"]).abs()

    # 2. Auswertung inkl. rechtszensierter 'overfull'-Zeilen
    te_all = test_folge.join(r_tr_full, on=["Location_id", "material_type"]).dropna(
        subset=["rate_med"]
    )
    pred_raw = te_all["rate_med"] * te_all["abstand"]
    pred_clip = pred_raw.clip(upper=100.0)
    f_oos_zens = pd.Series(
        np.where(
            ~te_all["ueber"],
            (pred_clip - te_all["p"]).abs(),
            np.maximum(0.0, 100.0 - pred_raw),
        ),
        index=te_all.index,
    )

    return {
        "stichtag": str(stichtag_ts.date()),
        "n_test_numerisch": len(f_oos_num),
        "n_test_zensiert": len(f_oos_zens),
        "oos_fehler_median_pp": float(f_oos_num.median()),
        "oos_fehler_p90_pp": float(f_oos_num.quantile(0.9)),
        "oos_fehler_mittel_pp": float(f_oos_num.mean()),
        "oos_anteil_bis_10_pp": float((f_oos_num <= 10.0).mean()),
        "oos_zensiert_median_pp": float(f_oos_zens.median()),
        "oos_zensiert_p90_pp": float(f_oos_zens.quantile(0.9)),
        "oos_zensiert_mittel_pp": float(f_oos_zens.mean()),
        "oos_zensiert_anteil_bis_10_pp": float((f_oos_zens <= 10.0).mean()),
    }


if __name__ == "__main__":
    daten = lade_messungen()
    raten = schaetze_fuellraten(daten)
    sim = simuliere_puffer(daten, raten)
    kz = bilanz_kennzahlen(sim)
    bt = backtest_zeitlich(daten)
    print(
        f"In-Sample numerisch (n={kz['folgemessungen_numerisch']}): "
        f"Median={kz['fehler_median_pp']:.1f} Pp | "
        f"P90={kz['fehler_p90_pp']:.1f} Pp | "
        f"Mittel={kz['fehler_mittel_pp']:.1f} Pp"
    )
    print(
        f"In-Sample inkl. zensiert (n={kz['folgemessungen_gesamt']}): "
        f"Median={kz['fehler_zensiert_median_pp']:.1f} Pp | "
        f"P90={kz['fehler_zensiert_p90_pp']:.1f} Pp | "
        f"Mittel={kz['fehler_zensiert_mittel_pp']:.1f} Pp"
    )
    print(
        f"Backtest > {bt['stichtag']} (n={bt['n_test_numerisch']}): "
        f"Median={bt['oos_fehler_median_pp']:.1f} Pp | "
        f"P90={bt['oos_fehler_p90_pp']:.1f} Pp | "
        f"Mittel={bt['oos_fehler_mittel_pp']:.1f} Pp"
    )
