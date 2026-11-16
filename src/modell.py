"""Puffer-Modell je Container (Location_id, material_type).

Grundlage: docs/datenmodell.md, AGENTS.md (Annahmen A1-A4), scripts/fakten.py (Abschnitt 5 & 6).
Erlaubte Spalten: Location_id, material_type, date, fill_level_perc.

Modellgleichung je Container c = (Location_id, material_type):
- Abfluss (Leerung): Jede Messung (Location_id, material_type, date) leert den Puffer auf 0 % (A1, A4).
- Zufluss (Füllrate): Zwischen zwei Messungen mit Abstand dt (in Tagen) wächst der Stand
  linear mit konstanter täglicher Rate r_c (% pro Tag Wachstum, A2):
      y_hat = r_c * dt
      p_hat = min(r_c * dt, 100)
  Die Rate wird als clipping-bewusster MAE-Fit je Container geschätzt (Grid 0,05-6,0
  %/Tag, Schritt 0,05; Verlust über die unzensierten Folgemessungen:
  |clip(r*dt, 0, 100) - p|). Begründung und Klassenschranke 13,6 Pp:
  docs/grenzwerte.md §2, scripts/fakten.py Abschnitt 12.5; Entscheid Samuel 2026-11-16.
- Zensierung ('overfull', A3): 'overfull' ist rechtszensiert (wahrer Stand >= 100 %), nicht 100.
  In der Ratenschätzung wird 'overfull' nicht als 100 eingesetzt, sondern liefert die
  untere Schranke r_min = 100 / dt. Beim Nachrechnen ist der zensierte Fehler
  max(0, 100 - y_hat) (0 Pp, sobald y_hat >= 100 %).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from domaene import DEFAULT_CSV, ERLAUBTE_SPALTEN, lade_messungen  # noqa: F401 (Re-Export)

# Grenzwerte gemäß AGENTS.md §4 (von Samuel festgelegt)
GRENZWERT_MEDIAN_PP = 10.0
GRENZWERT_P90_PP = 37.0
# MAE ≤ 14,0 Pp (Samuel, 2026-11-16): Anker ist die zeilengewichtete Klassenschranke
# 13,6 Pp der Modellklasse "eine Rate je Container" (fakten.py Abschnitt 12.5 F,
# Oracle/clipping-bewusst) — unabhängig vom Modell-Ergebnis begründet, siehe
# docs/grenzwerte.md §1/§2. Der frühere Wert 12,0 lag unter dieser Klassenschranke
# und war damit in der Klasse prinzipiell unerreichbar.
GRENZWERT_MAE_PP = 14.0
GRENZWERT_OOS_MEDIAN_PP = 16.0
GRENZWERT_OOS_P90_PP = 50.0
UEBERLAUF_TOLERANZ_PP = 0.04

# Grid für den MAE-Fit der Rate: 0,05-6,0 %/Tag, Schritt 0,05 (fakten.py Abschnitt 12.5)
RATE_GRID = np.arange(0.05, 6.001, 0.05)


def rate_mae_fit(p_unzensiert: np.ndarray, abstand_unzensiert: np.ndarray) -> float:
    """Rate (%/Tag) mit minimalem MAE je Container auf RATE_GRID (clipping-bewusst).

    Verlust (nur unzensierte Folgemessungen, wie fakten.py Abschnitt 12.5 F):
    |clip(r * abstand, 0, 100) - p|. Zensierte 'overfull'-Zeilen fließen NICHT in
    den Fit ein (Messung 2026-11-16: mit Zensiert-Term im Verlust steigt P90 auf
    37,1 Pp > Grenzwert und die Überlaufquote auf 20,5 % — verworfen). Ohne
    unzensierte Folgemessung: NaN (Fallback unten: Untergrenze wie bisher).
    """
    if len(abstand_unzensiert) == 0:
        return float("nan")
    r = RATE_GRID[:, None]
    verlust = np.abs(
        np.clip(r * abstand_unzensiert[None, :], 0.0, 100.0) - p_unzensiert[None, :]
    ).sum(axis=1)
    return float(RATE_GRID[int(np.argmin(verlust))])


def _fit_gruppe(g: pd.DataFrame) -> float:
    """MAE-Fit für eine Container-Gruppe (Spalten p, ueber, abstand vorhanden)."""
    unz = g[(g["abstand"] > 0) & ~g["ueber"]]
    return rate_mae_fit(
        unz["p"].to_numpy(dtype=float),
        unz["abstand"].to_numpy(dtype=float),
    )


def schaetze_fuellraten(df: pd.DataFrame) -> pd.DataFrame:
    """Schätzt die Füllrate (% pro Tag) je Container (Location_id, material_type).

    - Primär `rate_fit`: clipping-bewusster MAE-Fit je Container (`rate_mae_fit`) über
      die unzensierten Folgemessungen. Ein Parameter je Container, gefittet auf den
      eigenen Zeilen — gleiche Anpassungsstufe wie der frühere Median der Quotienten,
      aber mit der Verlustfunktion MAE inkl. 100-%-Kappung (Klassenschranke 13,6 Pp,
      fakten.py Abschnitt 12.5 F).
    - Zensierte 'overfull'-Zeilen gehen NICHT in den Fit ein; Container ohne unzensierte
      Folgemessung bekommen wie bisher die Untergrenze `rate_zensiert_min_med`
      (Median von 100/abstand über 'overfull') als Fallback.
    - Diagnostik bleibt erhalten:
      `rate_unzensiert_med` = Median der Quotienten p/abstand über unzensierte
      Folgemessungen; `rate_zensiert_min_med` = Median der Untergrenze 100/abstand
      über zensierte Folgemessungen (Fallback alter Semantik).
    - Container ohne verwertbare Folgemessung: NaN.
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
    fit = grp.apply(_fit_gruppe, include_groups=False)
    basis["rate_fit"] = fit.combine_first(basis["rate_zensiert_min_med"])
    basis["tage_bis_100"] = 100.0 / basis["rate_fit"].where(basis["rate_fit"] > 0)
    return basis


def simuliere_puffer(
    df: pd.DataFrame, raten: pd.DataFrame | pd.Series | None = None
) -> pd.DataFrame:
    """Rechnet den Puffer je (Location_id, material_type) nach.

    - Abfluss: Nach jeder Messung startet der Puffer bei 0 % (`stand_nach_leerung = 0.0`).
    - Zufluss: Bis zur nächsten Messung nach `abstand` Tagen fließt `pred_raw = rate_fit * abstand` zu.
    - Gedeckelter Skalenwert: `pred = min(pred_raw, 100.0)`.
    - Fehler (Prozentpunkte):
      * `fehler_numerisch`: |pred - p| auf unzensierten Folgemessungen (~ueber & abstand > 0).
      * `fehler_zensiert`: |pred - p| für numerische Messungen, und max(0, 100 - pred_raw)
        für rechtszensierte 'overfull'-Messungen (wahrer Wert >= 100 %).
    """
    if raten is None:
        raten_df = schaetze_fuellraten(df)
        rate_ser = raten_df["rate_fit"].rename("rate_fit")
    elif isinstance(raten, pd.DataFrame):
        rate_ser = raten["rate_fit"].rename("rate_fit")
    else:
        rate_ser = raten.rename("rate_fit")

    sim = df.join(rate_ser, on=["Location_id", "material_type"]).copy()
    sim["stand_nach_leerung"] = 0.0
    sim["pred_raw"] = sim["rate_fit"] * sim["abstand"]
    sim["pred"] = sim["pred_raw"].clip(upper=100.0)
    sim["pred_ab_100"] = sim["pred_raw"] >= 100.0
    sim["pred_ueber_100"] = sim["pred_raw"] > 100.0
    sim["pred_ueber"] = sim["pred_raw"] > 110.0

    ist_folge = (sim["abstand"] > 0) & sim["rate_fit"].notna()
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


def simuliere_beobachtungsmodell(
    df: pd.DataFrame, raten: pd.DataFrame | pd.Series | None = None
) -> pd.DataFrame:
    """Simuliert die beobachteten Füllstände auf dem echten Besuchsplan.

    Die Zeilen von ``df`` sind bereits genau die tatsächlich gemessenen Farben bei
    tatsächlich stattgefundenen Besuchen; fehlende Farben werden daher nicht ergänzt.
    Der modellierte Stand wächst ab der letzten Messung derselben Kammer, wird auf
    die 10-Prozent-Auflösung gerundet und ab 100 % als ``overfull`` zensiert (A3).
    """
    sim = simuliere_puffer(df, raten).copy()
    sim["sim_fill_level_perc"] = np.where(
        sim["pred_raw"] >= 100.0,
        "overfull",
        (sim["pred_raw"] / 10.0).round() * 10.0,
    )
    sim["sim_p_untergrenze"] = (sim["pred_raw"] / 10.0).round() * 10.0
    sim.loc[sim["pred_raw"] >= 100.0, "sim_p_untergrenze"] = 100.0
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
    # (MAE-Fit, identisch zu schaetze_fuellraten)
    r_tr = (
        train_folge.groupby(["Location_id", "material_type"])
        .apply(_fit_gruppe, include_groups=False)
        .rename("rate_fit")
    )

    # 1. Numerische Auswertung
    te_num = test_folge[~test_folge["ueber"]].join(
        r_tr.rename("rate_tr"), on=["Location_id", "material_type"]
    ).dropna(subset=["rate_tr"])
    f_oos_num = ((te_num["rate_tr"] * te_num["abstand"]).clip(upper=100.0) - te_num["p"]).abs()

    # 2. Auswertung inkl. rechtszensierter 'overfull'-Zeilen
    te_all = test_folge.join(r_tr, on=["Location_id", "material_type"]).dropna(
        subset=["rate_fit"]
    )
    pred_raw = te_all["rate_fit"] * te_all["abstand"]
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
