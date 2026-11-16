#!/usr/bin/env python3
"""Berechnet alle Fakten aus der Original-CSV. Jede Zahl in README.md/AGENTS.md stammt von hier.
Aufruf: python scripts/fakten.py [pfad_zur_csv]"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

CSV = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "data" / "raw" / "glass_fill_levels_anonymized_f.csv"
d = pd.read_csv(CSV, parse_dates=["date"])
def h(t): print(f"\n== {t}")

h("1 Form")
print("Spalten:", list(d.columns), "| Typen:", dict(d.dtypes.astype(str)))
print("Zeilen:", len(d), "| fehlende Werte:", int(d.isna().sum().sum()), "| exakte Duplikate:", int(d.duplicated().sum()))
print("Zeitraum:", d.date.min().date(), "bis", d.date.max().date(), "| Tage:", (d.date.max() - d.date.min()).days)
print("Zeitstempel hat Uhrzeit:", bool((d.date != d.date.dt.normalize()).any()), "(nur Datum, keine Uhrzeit)")

h("2 Füllstand: Werte")
print(d.fill_level_perc.value_counts().sort_index().to_string())
d["ueber"] = d.fill_level_perc.eq("overfull")
d["p"] = pd.to_numeric(d.fill_level_perc.where(~d.ueber))
print("Numerisch > 100:", int((d.p > 100).sum()), "| Zeile 'overfull' (Text):", int(d.ueber.sum()), f"= {d.ueber.mean():.1%}")
print("Genau 100:", int((d.p == 100).sum()), f"= {(d.p == 100).mean():.1%}", "| Genau 0:", int((d.p == 0).sum()))
print("Stufen numerisch:", sorted(d.p.dropna().unique().astype(int).tolist()))

h("3 Container-IDs und Glasarten")
print("Container-IDs:", d.Location_id.nunique(), "| Container+Farbe:", d.groupby(["Location_id", "material_type"]).ngroups)
print("Messungen je Farbe:\n" + d.material_type.value_counts().to_string())
print("Überlauf-Anteil je Farbe:\n" + d.groupby("material_type").ueber.mean().map("{:.1%}".format).to_string())
print("Farben pro ID (Anzahl IDs):", d.groupby("Location_id").material_type.nunique().value_counts().sort_index().to_dict())
print("Doppelte (ID,Farbe,Datum):", int(d.duplicated(["Location_id", "material_type", "date"]).sum()))

h("4 Besuche (ID+Datum = ein LKW-Besuch, Annahme)")
v = d.groupby(["Location_id", "date"]).material_type.nunique().rename("farben").reset_index().sort_values(["Location_id", "date"])
print("Besuche:", len(v), "| Farben je Besuch (Anzahl Besuche):", v.farben.value_counts().sort_index().to_dict())
v["abstand"] = v.groupby("Location_id").date.diff().dt.days
print("Messungen je ID: Median", d.groupby("Location_id").size().median(), "min", d.groupby("Location_id").size().min(), "max", d.groupby("Location_id").size().max())
print("Besuche je ID: Median", v.groupby("Location_id").size().median(), "min", v.groupby("Location_id").size().min(), "max", v.groupby("Location_id").size().max())
print("Abstand zwischen Besuchen (Tage): min", v.abstand.min(), "P10", v.abstand.quantile(.1), "Median", v.abstand.median(), "P90", v.abstand.quantile(.9), "max", v.abstand.max())
print("Wochentage Messungen (0=Mo):", d.date.dt.dayofweek.value_counts().sort_index().to_dict())

h("5 Füllstand nach Abstand zum letzten Besuch (Container+Farbe)")
d = d.sort_values(["Location_id", "material_type", "date"])
d["abstand"] = d.groupby(["Location_id", "material_type"]).date.diff().dt.days
x = d.dropna(subset=["abstand"]).copy()
x["klasse"] = pd.cut(x.abstand, [0, 7, 14, 30, 60, 400], labels=["<=7", "8-14", "15-30", "31-60", ">60"])
print(x.groupby("klasse", observed=True).agg(n=("p", "size"), mittel_fuell=("p", "mean"), ueberlauf=("ueber", "mean")).round(3).to_string())
print("Erste Messung je Container+Farbe hat keinen Vorgänger:", int(d.abstand.isna().sum()))

h("6 Bilanz-Probe (Rate * Abstand = gemessener Stand?)")
ok = x[~x.ueber & (x.abstand > 0)].copy()
ok["rate"] = ok.p / ok.abstand
r = ok.groupby(["Location_id", "material_type"]).rate.median().rename("rate_med")
ok = ok.join(r, on=["Location_id", "material_type"])
ok["pred"] = (ok.rate_med * ok.abstand).clip(upper=100)
fehler = (ok.pred - ok.p).abs()
print("Zeilen für Probe:", len(ok), "| mittlerer Fehler (Prozentpunkte, in-sample):", round(fehler.mean(), 1), "| Median:", round(fehler.median(), 1), "| P90:", round(fehler.quantile(.9), 1))
print("Anteil Fehler <= 10 Pp:", f"{(fehler <= 10).mean():.1%}", "| <= 20 Pp:", f"{(fehler <= 20).mean():.1%}")
print("Rate %/Tag je Container+Farbe: P10", round(r.quantile(.1), 2), "Median", round(r.median(), 2), "P90", round(r.quantile(.9), 2))
print("Tage bis 100% bei Median-Rate (Median über Container+Farbe):", round((100 / r[r > 0]).median(), 1))
r_ov_lb = x[x.ueber & (x.abstand > 0)].assign(lb=100.0 / x.loc[x.ueber & (x.abstand > 0), "abstand"]).groupby(["Location_id", "material_type"]).lb.median()
r_full = r.combine_first(r_ov_lb).rename("rate_med")
x_mod = x[x.abstand > 0].join(r_full, on=["Location_id", "material_type"]).copy()
x_mod["pred_raw"] = x_mod.rate_med * x_mod.abstand
x_mod["pred_clip"] = x_mod.pred_raw.clip(upper=100.0)
fehler_zens = pd.Series(np.where(~x_mod.ueber, (x_mod.pred_clip - x_mod.p).abs(), np.maximum(0.0, 100.0 - x_mod.pred_raw)), index=x_mod.index)
print("Folgemessungen gesamt (abstand > 0):", len(x_mod), "| davon numerisch:", int((~x_mod.ueber).sum()), "| davon overfull (zensiert >=100%):", int(x_mod.ueber.sum()), "| overfull bei Erstmessung:", int(d.loc[d.abstand.isna(), "ueber"].sum()))
print("Container+Farbe mit Rate:", len(r_full), "(unzensiert:", len(r), "+ nur overfull-Untergrenze:", int(len(r_full) - len(r)), "| ohne Folgemessung:", int(d.groupby(["Location_id", "material_type"]).ngroups - len(r_full)), ")")
print("Fehler inkl. zensiert (n=10363, Pp): Mittel:", round(fehler_zens.mean(), 1), "| Median:", round(fehler_zens.median(), 1), "| P90:", round(fehler_zens.quantile(.9), 1), "| <= 10 Pp:", f"{(fehler_zens <= 10).mean():.1%}", "| <= 20 Pp:", f"{(fehler_zens <= 20).mean():.1%}")

# 6b Vergleich A1 streng (Abstand zum letzten Standort-Besuch statt zur letzten Farbmessung) + Out-of-Sample
v_loc = d[["Location_id", "date"]].drop_duplicates().sort_values(["Location_id", "date"])
v_loc["abstand_loc"] = v_loc.groupby("Location_id").date.diff().dt.days
d_loc = d.merge(v_loc, on=["Location_id", "date"], how="left")
ok_loc = d_loc.dropna(subset=["abstand_loc"])
ok_loc = ok_loc[~ok_loc.ueber & (ok_loc.abstand_loc > 0)].copy()
ok_loc["rate_loc"] = ok_loc.p / ok_loc.abstand_loc
r_loc_med = ok_loc.groupby(["Location_id", "material_type"]).rate_loc.median().rename("r_loc_med")
ok_loc = ok_loc.join(r_loc_med, on=["Location_id", "material_type"])
fehler_loc = ((ok_loc.r_loc_med * ok_loc.abstand_loc).clip(upper=100) - ok_loc.p).abs()
print("Messungen mit abstand_loc != abstand_farbe (fehlende Farbmessung beim Vorbesuch):", int((d_loc.abstand_loc != d_loc.abstand).dropna().sum()))
print("Bilanz mit Standort-Abstand (streng A1): mittlerer Fehler", round(fehler_loc.mean(), 1), "Pp | Median:", round(fehler_loc.median(), 1), "| <= 10 Pp:", f"{(fehler_loc <= 10).mean():.1%}")

mid_date = d.date.min() + (d.date.max() - d.date.min()) / 2
tr_ok = ok[ok.date <= mid_date]
te_ok = ok[ok.date > mid_date].copy()
r_tr = tr_ok.groupby(["Location_id", "material_type"]).rate.median().rename("rate_tr")
te_ok = te_ok.join(r_tr, on=["Location_id", "material_type"]).dropna(subset=["rate_tr"])
fehler_oos = ((te_ok.rate_tr * te_ok.abstand).clip(upper=100) - te_ok.p).abs()
print(f"Out-of-Sample (Training <= {mid_date.date()}, Test > {mid_date.date()}, n={len(te_ok)}): mittlerer Fehler", round(fehler_oos.mean(), 1), "Pp | Median:", round(fehler_oos.median(), 1), "| P90:", round(fehler_oos.quantile(.9), 1), "| <= 10 Pp:", f"{(fehler_oos <= 10).mean():.1%}")
tr_all = x_mod[x_mod.date <= mid_date]
r_tr_ov = (100.0 / tr_all.loc[tr_all.ueber, "abstand"]).groupby([tr_all.loc[tr_all.ueber, "Location_id"], tr_all.loc[tr_all.ueber, "material_type"]]).median()
r_tr_full = r_tr.combine_first(r_tr_ov).rename("rate_tr")
te_all = x_mod[x_mod.date > mid_date].join(r_tr_full, on=["Location_id", "material_type"]).dropna(subset=["rate_tr"]).copy()
te_all["pred_tr_raw"] = te_all.rate_tr * te_all.abstand
te_all["pred_tr_clip"] = te_all.pred_tr_raw.clip(upper=100.0)
f_oos_zens = pd.Series(np.where(~te_all.ueber, (te_all.pred_tr_clip - te_all.p).abs(), np.maximum(0.0, 100.0 - te_all.pred_tr_raw)), index=te_all.index)
print(f"Out-of-Sample inkl. zensiert (n={len(te_all)}): mittlerer Fehler", round(f_oos_zens.mean(), 1), "Pp | Median:", round(f_oos_zens.median(), 1), "| P90:", round(f_oos_zens.quantile(.9), 1), "| <= 10 Pp:", f"{(f_oos_zens <= 10).mean():.1%}")
d_fol = x[x.abstand > 0].join(r_full, on=["Location_id", "material_type"])
print("Überlauf-Quote auf Folgemessungen (n=10363): Daten", f"{d_fol.ueber.mean():.1%}", "| Modell >=100%:", f"{(d_fol.rate_med * d_fol.abstand >= 100).mean():.1%}", "| Modell >100%:", f"{(d_fol.rate_med * d_fol.abstand > 100).mean():.1%}", "| Modell >110%:", f"{(d_fol.rate_med * d_fol.abstand > 110).mean():.1%}")
print("Bilanztest-Grenzwerte (AGENTS.md §4): In-Sample Median <= 10.0 Pp, P90 <= 37.0 Pp, Mittel <= 14.0 Pp | Backtest Median <= 16.0 Pp, P90 <= 50.0 Pp.")

h("7 Container-Cluster nach Rhythmus (Tag <=1d, Woche 2-7d, Monat 8-30d, Quartal 31-90d, >Quartal >90d)")
v_ueber = d.groupby(["Location_id", "date"]).agg(hat_ueber=("ueber", "any"), max_p=("p", "max")).reset_index().sort_values(["Location_id", "date"])
v_ueber["abstand"] = v_ueber.groupby("Location_id").date.diff().dt.days
bins_c = [0, 1, 7, 30, 90, 1000]
labels_c = ["Tag (<=1d)", "Woche (2-7d)", "Monat (8-30d)", "Quartal (31-90d)", ">Quartal (>90d)"]
order_c = labels_c + ["Nur 1 Besuch"]
loc_c = v_ueber.groupby("Location_id").agg(
    besuche=("date", "size"),
    med_abstand=("abstand", "median"),
    ueberlauf_besuche=("hat_ueber", "sum"),
    mittel_max_p=("max_p", "mean"),
)
loc_c["ist_cluster"] = pd.cut(loc_c.med_abstand, bins_c, labels=labels_c).astype(object).fillna("Nur 1 Besuch")
r_loc_max = r.groupby("Location_id").max()
loc_c["tage_bis_80"] = 80.0 / r_loc_max.where(r_loc_max > 0)
loc_c["tage_bis_100"] = 100.0 / r_loc_max.where(r_loc_max > 0)
loc_c["bedarf_80"] = pd.cut(loc_c.tage_bis_80, bins_c, labels=labels_c).astype(object).fillna("Nur 1 Besuch")
loc_c["bedarf_100"] = pd.cut(loc_c.tage_bis_100, bins_c, labels=labels_c).astype(object).fillna("Nur 1 Besuch")

t_ist = loc_c.groupby(pd.Categorical(loc_c.ist_cluster, categories=order_c, ordered=True), observed=False).agg(
    container=("besuche", "size"),
    besuche=("besuche", "sum"),
    med_abstand=("med_abstand", "median"),
    ueberlauf_besuche=("ueberlauf_besuche", "sum"),
    mittel_max_fuell=("mittel_max_p", "mean"),
)
t_ist["ueberlauf_quote"] = (t_ist.ueberlauf_besuche / t_ist.besuche).fillna(0)
print("7.1 Ist-Cluster (nach Median-Besuchsabstand je Location_id):\n" + t_ist.round(3).to_string())

t_bed = pd.DataFrame({
    "bedarf_bis_80": pd.Categorical(loc_c.bedarf_80, categories=order_c, ordered=True).value_counts(),
    "bedarf_bis_100": pd.Categorical(loc_c.bedarf_100, categories=order_c, ordered=True).value_counts(),
})
print("\n7.2 Bedarfs-Cluster (schnellste Farbe je Location_id, A1+A2):\n" + t_bed.to_string())

ct_80 = pd.crosstab(
    pd.Categorical(loc_c.ist_cluster, categories=order_c, ordered=True),
    pd.Categorical(loc_c.bedarf_80, categories=order_c, ordered=True),
    margins=True,
)
ct_80.index.name = "Ist \\ Bedarf_80"
ct_80.columns.name = ""
print("\n7.3 Kreuztabelle Ist-Cluster vs. Bedarf bis 80%:\n" + ct_80.to_string())

loc_c["ist_code"] = pd.cut(loc_c.med_abstand, bins_c, labels=False)
loc_c["bed_code_80"] = pd.cut(loc_c.tage_bis_80, bins_c, labels=False)
loc_c["status_80"] = np.where(
    loc_c.ist_code.isna() | loc_c.bed_code_80.isna(),
    "Nur 1 Besuch",
    np.where(
        loc_c.ist_code < loc_c.bed_code_80,
        "Zu oft (Ist < Bedarf_80)",
        np.where(loc_c.ist_code > loc_c.bed_code_80, "Zu spaet (Ist > Bedarf_80)", "Passend (Ist == Bedarf_80)"),
    ),
)
loc_c["delta_besuche_80"] = (loc_c.besuche - 1) - np.floor((loc_c.besuche - 1) * loc_c.med_abstand / loc_c.tage_bis_80)
t_abw = loc_c.groupby("status_80").agg(
    container=("besuche", "size"),
    besuche_ist=("besuche", "sum"),
    ueberlauf_besuche=("ueberlauf_besuche", "sum"),
    med_abstand_ist=("med_abstand", "median"),
    tage_bis_80_med=("tage_bis_80", "median"),
    mittel_max_fuell=("mittel_max_p", "mean"),
    rechn_gesparte_besuche=("delta_besuche_80", "sum"),
)
t_abw["ueberlauf_quote"] = (t_abw.ueberlauf_besuche / t_abw.besuche_ist).fillna(0)
print("\n7.4 Abweichungs-Gruppen (40 zu oft vs. 18 zu spaet gegen 80%-Bedarf):\n" + t_abw.round(3).to_string())

h("8 Auswahleffekt-Prüfung (Zwischen Standorten vs. innerhalb desselben Standorts)")
x_sel = x[x.abstand > 0].join(r_full, on=["Location_id", "material_type"]).copy()
x_sel["med_abstand_id"] = x_sel.groupby(["Location_id", "material_type"]).abstand.transform("median")
x_sel["rate_obs"] = x_sel.p.fillna(100.0) / x_sel.abstand

q_between = x_sel.groupby("klasse", observed=True).agg(
    n=("abstand", "size"),
    mittel_fuell_num=("p", "mean"),
    ueberlauf=("ueber", "mean"),
    rate_dieser_messung_med=("rate_obs", "median"),
    standort_dauer_rate_med=("rate_med", "median"),
    standort_typ_abstand_med=("med_abstand_id", "median"),
)
print("8.1 Zwischen Standorten (Simpson-Paradoxon über die Abstandsklassen aus Abschnitt 5):\n" + q_between.round(2).to_string())

hat_kurz7 = x_sel.groupby(["Location_id", "material_type"]).abstand.min() <= 7
x_sel["hat_kurz7"] = x_sel.set_index(["Location_id", "material_type"]).index.map(hat_kurz7)
sub_k7 = x_sel[x_sel.hat_kurz7].copy()
sub_k7["gruppe"] = np.where(sub_k7.abstand <= 7, "Messung bei <=7d (n=291)", "Andere Messungen derselben Container (>7d)")
q_k7 = sub_k7.groupby("gruppe").agg(
    n=("abstand", "size"),
    abstand_med=("abstand", "median"),
    mittel_fuell_num=("p", "mean"),
    ueberlauf=("ueber", "mean"),
    rate_med=("rate_obs", "median"),
)
print("\n8.2 Container, die mindestens einmal bei <=7 Tagen geleert wurden (im Kurz-Intervall vs. sonst):\n" + q_k7.round(2).to_string())

x_sel["rel_abstand"] = x_sel.abstand / x_sel.med_abstand_id
x_sel["rel_klasse"] = pd.cut(
    x_sel.rel_abstand,
    [0, 0.5, 0.8, 1.2, 1.5, 20],
    labels=["<0.5x (viel frueher)", "0.5-0.8x (frueher)", "0.8-1.2x (normal)", "1.2-1.5x (spaeter)", ">1.5x (viel spaeter)"],
)
x_sel["rate_faktor_zu_standort"] = x_sel.rate_obs / x_sel.rate_med
q_within = x_sel.groupby("rel_klasse", observed=True).agg(
    n=("abstand", "size"),
    abstand_med=("abstand", "median"),
    mittel_fuell_num=("p", "mean"),
    med_fuell_num=("p", "median"),
    ueberlauf=("ueber", "mean"),
    rate_med=("rate_obs", "median"),
    faktor_zu_standort_rate_med=("rate_faktor_zu_standort", "median"),
)
print("\n8.3 Innerhalb desselben Standorts (relativer Abstand abstand / med_abstand_id):\n" + q_within.round(2).to_string())

h("9 Leerung: Messwert liegt VOR der Leerung, danach Start bei 0")
d_p = d.sort_values(["Location_id", "material_type", "date"]).copy()
g_p = d_p.groupby(["Location_id", "material_type"])
d_p["p_prev"] = g_p.p.shift()
d_p["abstand_f"] = g_p.date.diff().dt.days
paare = d_p[d_p.abstand_f.gt(0) & d_p.p.notna() & d_p.p_prev.notna()].copy()
print("Paare mit numerischem Vorgaengerstand:", len(paare),
      "| Stand niedriger als beim Vorgaenger:", f"{(paare.p < paare.p_prev).mean():.1%}",
      "| Median-Abfall:", round((paare.p_prev - paare.p).median(), 1), "Pp")
paare["rate"] = paare.p / paare.abstand_f
paare["rate_med"] = paare.groupby(["Location_id", "material_type"]).rate.transform("median")
for name, pred in [
    ("A1/A4 (Start 0 nach Besuch)", (paare.rate_med * paare.abstand_f).clip(upper=100.0)),
    ("ohne Leerung (Wachstum ab Vorgaengerstand)", (paare.p_prev + paare.rate_med * paare.abstand_f).clip(upper=100.0)),
]:
    e = (pred - paare.p).abs()
    print(f"{name}: Median-Fehler {e.median():.1f} Pp | Mittel {e.mean():.1f} Pp | <= 10 Pp: {(e <= 10).mean():.1%}")

h("10 Saisonalität der Füllrate (A2-Jahreskonstanz prüfen)")
sa = ok[ok.rate_med > 0].copy()
print("Basis: Abschnitt 6 (numerische Folgemessungen, Zeilen ohne Container-Rate entfernt):", len(sa))
sa["rel"] = sa.rate / sa.rate_med
sa["monat"] = sa.date.dt.month
m10 = sa.groupby("monat", observed=True).agg(
    n=("rel", "size"),
    median_rel=("rel", "median"),
    q10=("rel", lambda s: s.quantile(0.10)),
    q90=("rel", lambda s: s.quantile(0.90)),
)
print("Relative Rate je Monat (1,0 = Jahresmedian desselben Containers):\n" + m10.round(3).to_string())
print("Spanne der Monats-Mediane:", round(m10.median_rel.min(), 3), "bis", round(m10.median_rel.max(), 3))
sa["wt"] = sa.date.dt.day_of_week
wt10 = sa.groupby("wt", observed=True).agg(n=("rel", "size"), median_rel=("rel", "median"))
print("Relative Rate je Wochentag (0 = Montag):\n" + wt10.round(3).to_string())
print("Befund: Monats-Mediane bleiben nahe 1,0 — kein messbarer Jahresgang (Okt nur Randmonat, Sa wenig n). "
      "A2-Jahreskonstanz gestützt; Saisonalität bleibt unmodelliert.")

h("11 Reparatur-Diagnose: MAE je Farbe und Fehler nach Abstandsklasse (nur Messung, kein Modellwechsel)")
ok["fehler"] = (ok["pred"] - ok["p"]).abs()
ok["rel"] = ok["rate"] / ok["rate_med"]
print("Referenz: Gesamt-MAE (Abschnitt 6):", round(ok.fehler.mean(), 1), "Pp bei n =", len(ok))
f11 = ok.groupby("material_type", observed=True).agg(
    n=("fehler", "size"),
    mae=("fehler", "mean"),
    median_fehler=("fehler", "median"),
    anteil_gesamt_mae=("fehler", lambda s: s.sum() / ok.fehler.sum()),
    pred_mittel=("pred", "mean"),
    echt_mittel=("p", "mean"),
)
print("(a) Fehler je Farbe — pred_mittel > echt_mittel heisst: Modell sagt zu viel Fuellung voraus:\n"
      + f11.round(2).to_string())
g11 = ok.groupby("klasse", observed=True).agg(
    n=("fehler", "size"),
    mae=("fehler", "mean"),
    median_fehler=("fehler", "median"),
    median_rel=("rel", "median"),
)
print("(b) Fehler und relative Rate nach Abstandsklasse (rel = rate / rate_med desselben Containers;\n"
      "     median_rel deutlich ueber 1 bei kurzen Abstaenden = Auswahleffekt im Fehler):\n"
      + g11.round(3).to_string())

h("12 Schätzer-Vergleich: Rate aus Quotienten-Median vs. Poolung (Messung, kein Modellwechsel)")
print("Hintergrund (Owner 2026-11-16): Der reale Plan ist eine dumm feste Route — Besuche reagieren")
print("nicht auf den Füllstand. Die Rate-Abstand-Korrelation (Abschnitt 11b) ist damit Beobachtungs-")
print("Artefakt (10er-Quantisierung bei kurzen Abständen), keine Füllsteuerung. Der Schätzer ist verdächtig, nicht die Dynamik.")
kurz = sa[sa.abstand <= 7]
print("Quantiserungs-Floor: Median p bei Abstand <=7d:", kurz.p.median(), "% | min:", kurz.p.min(), "% | Anteil p == 10:", f"{(kurz.p == 10).mean():.1%}")
CUTOFF = pd.Timestamp("2026-04-09")            # Backtest-Grenze wie AGENTS.md §4.4
train = sa[sa.date <= CUTOFF]
test = sa[sa.date > CUTOFF]
print("Schätzer jeweils NUR aus Trainingszeilen (<= 2026-04-09); n Train:", len(train), "| n Test:", len(test))
def bewerte(rate_map, name):
    r = sa.join(rate_map.rename("rate_est"), on=["Location_id", "material_type"])
    ohne = r.rate_est.isna().sum()
    r = r.dropna(subset=["rate_est"]).copy()
    r["pred"] = (r.rate_est * r.abstand).clip(upper=100)
    r["fehler"] = (r["pred"] - r.p).abs()
    ins = r[r.date <= CUTOFF].fehler
    oos = r[r.date > CUTOFF].fehler
    print(f"{name}: Container mit Rate {r.groupby(['Location_id','material_type']).ngroups} | ohne Rate {ohne} | "
          f"In-Sample MAE {ins.mean():.1f} | OOS MAE {oos.mean():.1f} | OOS Median {oos.median():.1f} | OOS P90 {oos.quantile(.9):.1f}")
bewerte(train.groupby(["Location_id", "material_type"]).rate.median(), "A Median der Quotienten (heutiges Modell)")
pooled = train.groupby(["Location_id", "material_type"]).apply(lambda g: g.p.sum() / g.abstand.sum(), include_groups=False)
bewerte(pooled, "B Poolung sum(p)/sum(abstand)")
ohne_kurz = train[train.abstand > 7].groupby(["Location_id", "material_type"]).rate.median()
bewerte(ohne_kurz, "C Median der Quotienten ohne Abstand <=7d")
ohne_lang = train[train.abstand <= 60].groupby(["Location_id", "material_type"]).rate.median()
bewerte(ohne_lang, "D Median der Quotienten ohne Abstand >60d")

h("12.1 Feinsplit kurze Abstände: Wird bei kurzen Abständen überhaupt geleert? (Messung)")
fs = sa[sa.abstand <= 7].copy()
fs["gap"] = pd.cut(fs.abstand, [0, 1, 2, 3, 5, 7], labels=["1", "2", "3", "4-5", "6-7"])
t121 = fs.groupby("gap", observed=True).agg(
    n=("p", "size"),
    median_p=("p", "median"),
    p10_p=("p", lambda s: s.quantile(0.1)),
    anteil_p_unter_20=("p", lambda s: (s < 20).mean()),
    median_rate=("rate", "median"),
    median_rate_med=("rate_med", "median"),
)
print("Kurze Abstände im Detail (rate = p/abstand, rate_med = Container-Median):\n" + t121.round(2).to_string())
print("Anteil kurzer Abstände mit p >= 30 % (unter A4+A2 mit Rate ~2,1 %/Tag kaum erklärbar):", f"{(fs.p >= 30).mean():.1%}")

h("12.2 Schätzer auf allen Zeilen (Semantik wie Bilanztest In-Sample) und OOS (Train-Zeitraum)")
def bewerte_full(rate_map, name):
    r = sa.join(rate_map.rename("rate_est"), on=["Location_id", "material_type"])
    ohne = int(r.rate_est.isna().sum())
    r = r.dropna(subset=["rate_est"]).copy()
    r["pred"] = (r.rate_est * r.abstand).clip(upper=100)
    r["fehler"] = (r["pred"] - r.p).abs()
    print(f"{name}: ohne Rate {ohne} | MAE über alle Zeilen {r.fehler.mean():.1f} | Median {r.fehler.median():.1f} | P90 {r.fehler.quantile(.9):.1f} (n={len(r)})")
bewerte_full(sa.groupby(["Location_id", "material_type"]).rate.median(), "A Median der Quotienten (heutiges Modell)")
bewerte_full(sa[sa.abstand > 7].groupby(["Location_id", "material_type"]).rate.median(), "C Median ohne <=7d (Fallback fehlender Container: ausgeschlossen)")
ohne_kurz_fb = sa[sa.abstand > 7].groupby(["Location_id", "material_type"]).rate.median()
bewerte_full(ohne_kurz_fb.combine_first(sa.groupby(["Location_id", "material_type"]).rate.median()), "C2 Median ohne <=7d, Fallback: Median aller Quotienten")

h("12.3 Erreichbarkeits-Schranke: Wie tief kann MAE in der Klasse 'eine Rate je Container' überhaupt? (Messung)")
print("Hintergrund: Owner 2026-11-16: 'Leert immer' — A1 exakt. Kurz-Abstand-Zeilen sind Anomalien oder")
print("Rate-Spitzen, nicht Nicht-Leerungen. Frage: Welches MAE-Minimum hat die Modellklasse 'konstante Rate je Container+Farbe'?")
def bestes_k():
    p_ = sa.p.to_numpy(); g_ = sa.abstand.to_numpy(); r_ = sa.rate_med.to_numpy()
    best = None
    for k in np.arange(0.50, 1.51, 0.01):
        pred = np.clip(k * r_ * g_, 0, 100)
        mae = np.abs(pred - p_).mean()
        if best is None or mae < best[1]: best = (round(float(k), 2), float(mae))
    return best
k, mae_k = bestes_k()
print(f"Globale Skala k*: {k} -> MAE {mae_k:.1f} Pp (pred = clip(k * rate_med * abstand, 0, 100))")
ora = sa.groupby(["Location_id", "material_type"]).apply(
    lambda g: np.min([np.abs(np.clip(r * g.abstand.to_numpy(), 0, 100) - g.p.to_numpy()).mean()
                      for r in np.arange(0.05, 6.01, 0.05)]), include_groups=False)
mae_oracle = ora.mean()
print(f"Oracle je Container (beste Rate pro Container, in-sample geschummelt — untere Schranke der Klasse): MAE {mae_oracle:.1f} Pp")
print("Lesart: Auch das betrügerisch optimale 'eine Rate je Container' liegt bei "
      f"{mae_oracle:.1f} Pp. Alles darüber braucht mehr als eine konstante Rate je Container.")

h("12.4 MAE-optimaler Schätzer: abstandsgewichteter Median (Gewicht = Abstand) — Messung vor dem Wechsel")
print("Begründung: min_r sum |r*gap_i - p_i| wird vom gewichteten Median der Quotienten (Gewicht gap_i) gelöst.")
print("Das ist der MAE-optimale Schätzer INNERHALB der Klasse 'eine Rate je Container' — kein Tuning, geschlossene Lösung.")
def wmedian(g, wert, gewicht):
    g = g.sort_values(wert)
    w = g[gewicht].to_numpy()
    cw = np.cumsum(w)
    return float(g[wert].to_numpy()[np.searchsorted(cw, cw[-1] / 2)])
def rate_wmed(dfr):
    return dfr.groupby(["Location_id", "material_type"]).apply(
        lambda g: wmedian(g[["rate", "abstand"]], "rate", "abstand"), include_groups=False)
def bewerte_map(rate_map, name):
    r = sa.join(rate_map.rename("rate_est"), on=["Location_id", "material_type"])
    ohne = int(r.rate_est.isna().sum())
    r = r.dropna(subset=["rate_est"]).copy()
    r["pred"] = (r.rate_est * r.abstand).clip(upper=100)
    r["fehler"] = (r["pred"] - r.p).abs()
    print(f"{name}: ohne Rate {ohne} | MAE alle Zeilen {r.fehler.mean():.1f} | Median {r.fehler.median():.1f} | "
          f"P90 {r.fehler.quantile(.9):.1f} | OOS MAE {r[r.date > CUTOFF].fehler.mean():.1f} "
          f"| OOS Median {r[r.date > CUTOFF].fehler.median():.1f} | OOS P90 {r[r.date > CUTOFF].fehler.quantile(.9):.1f}")
bewerte_map(rate_wmed(sa), "E gewichteter Median, alle Zeilen (In-Sample-Semantik wie Bilanztest)")
bewerte_map(rate_wmed(train), "E2 gewichteter Median, nur Trainingszeitraum")
bewerte_map(train.groupby(["Location_id", "material_type"]).rate.median(), "Referenz A2: ungewichteter Median, nur Train")

h("12.5 Clipping-bewusster MAE-Schätzer: pro Container die Rate mit minimalem MAE (gleiche Fit-Semantik wie der Median)")
print("Gleiches Anpassungsniveau wie rate_med: ein Parameter je Container, gefittet auf den eigenen Zeilen.")
print("Unterschied zur Referenz: Verlustfunktion MAE mit Clip bei 100 statt Median der Quotienten.")
def rate_mae_opt(dfr):
    def eins(g):
        g_ = np.arange(0.05, 6.001, 0.05)
        p = g.p.to_numpy(); ab = g.abstand.to_numpy()
        maes = [np.abs(np.clip(r * ab, 0, 100) - p).mean() for r in g_]
        return float(g_[int(np.argmin(maes))])
    return dfr.groupby(["Location_id", "material_type"]).apply(eins, include_groups=False)
bewerte_map(rate_mae_opt(sa), "F MAE-optimal je Container, alle Zeilen (In-Sample-Semantik wie Bilanztest)")
bewerte_map(rate_mae_opt(train), "F2 MAE-optimal je Container, nur Trainingszeitraum")

h("13 Diagnose Schätzer-Wechsel: Warum erzeugt der MAE-Fit mehr Überlauf? (Messung)")
import sys as _sys
_sys.path.insert(0, "src")
from modell import rate_mae_fit  # noqa: E402
rate_fit_map = ok.groupby(["Location_id", "material_type"]).apply(
    lambda g: rate_mae_fit(g.p.to_numpy(dtype=float), g.abstand.to_numpy(dtype=float)),
    include_groups=False,
)
cmp13 = ok.join(rate_fit_map.rename("rate_fit"), on=["Location_id", "material_type"])
cmp13["hoeher"] = cmp13.rate_fit > cmp13.rate_med
print(f"(a) rate_fit vs. rate_med (Median der Quotienten): Median rate_fit {cmp13.rate_fit.median():.2f} "
      f"vs. rate_med {cmp13.rate_med.median():.2f} | P90 {cmp13.rate_fit.quantile(.9):.2f} vs. "
      f"{cmp13.rate_med.quantile(.9):.2f} | Anteil Container mit rate_fit > rate_med: {cmp13.groupby(['Location_id','material_type']).hoeher.first().mean():.1%}")
for est, col in [("rate_med", "pred_m"), ("rate_fit", "pred_f")]:
    cmp13[col] = (cmp13[est] * cmp13.abstand)
folge13 = cmp13[cmp13.abstand > 0]
print(f"(b) Überlauf-Quote auf Folgemessungen (pred_raw > 110): Median-Schätzer "
      f"{(folge13.pred_m > 110).mean():.1%} | MAE-Fit {(folge13.pred_f > 110).mean():.1%} | Daten {folge13.ueber.mean():.1%}")
q13 = folge13.groupby("material_type", observed=True).agg(
    ueber_daten=("ueber", "mean"),
    ueber_med=("pred_m", lambda s: (s > 110).mean()),
    ueber_fit=("pred_f", lambda s: (s > 110).mean()),
)
print("(c) je Farbe:\n" + q13.round(3).to_string())
d13 = folge13[folge13.ueber].copy()
d13["med_ge_100"] = d13.pred_m >= 100
d13["fit_ge_100"] = d13.pred_f >= 100
print(f"(d) Auf echten Überlauf-Zeilen (n={len(d13)}): pred>=100 Median-Schätzer {d13.med_ge_100.mean():.1%} "
      f"| MAE-Fit {d13.fit_ge_100.mean():.1%}")
n13 = folge13[~folge13.ueber]
print(f"(e) Auf numerischen Folgemessungen (n={len(n13)}): falsch >110 Median-Schätzer "
      f"{(n13.pred_m > 110).mean():.1%} | MAE-Fit {(n13.pred_f > 110).mean():.1%}")

h("13.1 Mechanismus: Inflationiert die Gratis-Plattform bei p nahe 100 den MAE-Fit? (Messung)")
print("Hintergrund: |clip(r*dt,0,100) - p| ist fuer p=100 fuer ALLE r >= 100/dt exakt 0 —")
print("hohe Raten kosten an solchen Zeilen nichts, waehrend der Median durch Quotienten beschraenkt bleibt.")
rows_hi = cmp13[cmp13.p >= 90]
print(f"Anteil numerischer Zeilen mit p >= 90: {len(rows_hi)/len(cmp13):.1%} (n={len(rows_hi)}); p == 100 exakt: {(cmp13.p == 100).mean():.2%}")
grp13 = cmp13.groupby(["Location_id", "material_type"]).agg(
    rate_fit=("rate_fit", "first"), rate_med=("rate_med", "first"),
    anteil_p90=("p", lambda s: (s >= 90).mean()),
)
grp13["inflation"] = grp13.rate_fit / grp13.rate_med
b13 = grp13.groupby(pd.cut(grp13.anteil_p90, [-0.01, 0.001, 0.2, 0.5, 1.0],
                           labels=["keine p>=90", "0-20 %", "20-50 %", ">50 %"]), observed=True).agg(
    n=("inflation", "size"),
    median_inflation=("inflation", "median"),
    anteil_inflationiert=("inflation", lambda s: (s > 1.2).mean()),
)
print("(a) Inflation (rate_fit/rate_med) nach Anteil p>=90-Zeilen im Container:\n" + b13.round(2).to_string())

h("13.2 Ist die exakte 100-Lesung eine verdeckte Zensierung? (Messung, kein Modellwechsel)")
p_v = cmp13.p.value_counts().sort_index(ascending=False)
print("(a) Top-Fuellstaende nach Haeufigkeit (Anteil an 9.206 numerischen Zeilen):")
print((p_v.head(8) / len(cmp13)).round(4).to_string())
hi = cmp13[cmp13.p >= 90]
print(f"(b) Abstand-Median: p==100-Zeilen {cmp13[cmp13.p == 100].abstand.median():.0f} Tage "
      f"| p in 80-90 {cmp13[(cmp13.p >= 80) & (cmp13.p < 90)].abstand.median():.0f} | p < 80 {cmp13[cmp13.p < 80].abstand.median():.0f}")
p100 = cmp13[cmp13.p == 100]
print(f"(c) p==100-Zeilen mit Modell-pred (rate_med*abstand) < 100: {(p100.pred_m < 100).mean():.1%} "
      f"(n={len(p100)}) — unter A1/A2 waeren diese Lesungen ohne Zensierungs-Lesart 'zu voll'")
