#!/usr/bin/env python3
"""Erzeugt die Befund-Bilder aus der Original-CSV.

Aufruf: python scripts/bilder.py
Ausgabe in bilder/:
  01_mechanismus.png   ein Ort, drei Farben, ein Besuch
  02_alle_orte.png     449 Orte als Rangprofil, ohne Karte
  03_einheit.png       dieselben Daten, zwei Einheiten
  04_takt.png          Füllstand und Überlauf nach Abstand

Keine Modellannahme außer A1 (Besuch leert auf 0) und A2 (gleichmäßige Füllung),
beide im Bild benannt. Kein Raum, keine Prognose, keine Glättung, keine Zahl von Hand.
Regeln: assets/ui/UI_REGELN.md
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "raw" / "glass_fill_levels_anonymized_f.csv"
OUT = ROOT / "bilder"
OUT.mkdir(exist_ok=True)

C_FRUEH, C_PASST, C_UEBER = "#2F6FD0", "#8A8F98", "#B3261E"
MARKE = {"zu frueh": "o", "passt": "s", "uebervoll": "^"}
FARBE = {"zu frueh": C_FRUEH, "passt": C_PASST, "uebervoll": C_UEBER}
GLAS = {"brown": ("Braun", "#6B4226"), "green": ("Grün", "#1E7A3C"), "white": ("Weiß", "#3F3F3F")}
MON = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
KLASSE_TEXT = {"zu frueh": "zu früh (< 50 %)", "passt": "passt (50–99 %)", "uebervoll": "übervoll (≥ 100 %)"}

SCHWELLE_FRUEH = 50   # Anzeige-Grenze, keine Modellannahme
SCHWELLE_UEBER = 100  # overfull ist zensiert: Wert unbekannt, mindestens 100


def zt(n):
    return f"{n:,}".replace(",", ".")


def lade():
    d = pd.read_csv(CSV, parse_dates=["date"])
    d["ueber"] = d.fill_level_perc.eq("overfull")
    d["p"] = pd.to_numeric(d.fill_level_perc.where(~d.ueber))
    d["v"] = np.where(d.ueber, 100.0, d.p)
    d["klasse"] = np.where(d.ueber, "uebervoll",
                           np.where(d.p < SCHWELLE_FRUEH, "zu frueh", "passt"))
    return d


def monats_ticks(ax, d):
    ticks = [t for t in pd.date_range(d.date.min().replace(day=1), d.date.max(), freq="MS")
             if (t.month - 1) % 2 == 0]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{MON[t.month - 1]} {t.year % 100:02d}" for t in ticks], fontsize=11)


def leinwand(titel, unter, quelle, top=0.82, left=0.075, right=0.965, bottom=0.095):
    fig = plt.figure(figsize=(16, 9), dpi=100)
    fig.text(0.012, 0.975, titel, fontsize=19, weight="bold", ha="left", va="top")
    fig.text(0.012, 0.925, unter, fontsize=12.2, color="#333333", ha="left", va="top", linespacing=1.45)
    fig.text(0.012, 0.014, quelle, fontsize=8.8, color="#666666", ha="left", va="bottom")
    fig.subplots_adjust(left=left, right=right, top=top, bottom=bottom)
    return fig


def rahmen(ax, achse="y"):
    ax.grid(axis=achse, color="#E8E8E8", lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


# ---------------------------------------------------------------- Bild 1 ----
def bild_mechanismus(d):
    g = (d.groupby(["Location_id", "material_type"])
           .agg(n=("v", "size"), m=("v", "mean")).reset_index())
    n = g.pivot(index="Location_id", columns="material_type", values="n")
    m = g.pivot(index="Location_id", columns="material_type", values="m")
    ok = [i for i in n.dropna().index if (n.loc[i] >= 12).all()]
    lid = (m.loc[ok, "white"] - m.loc[ok, "brown"]).idxmax()
    s = d[d.Location_id == lid].sort_values("date")

    fig = leinwand(
        "Ein Ort, drei Farben — derselbe Besuch ist für Braun zu früh und für Weiß zu spät",
        f"Ort {lid[:8]}… · {len(s)} Ablesungen · jeder Punkt ist eine Messung beim Besuch.\n"
        "Gepunktet: Leerung auf 0 und Wiederanstieg — Annahmen A1/A2, dazwischen wurde nichts gemessen.",
        "Quelle: data/raw/glass_fill_levels_anonymized_f.csv · scripts/bilder.py · "
        "11.701 Messungen, 17.10.2025–30.09.2026 · Klassen sind Anzeige-Grenzen",
        top=0.80)
    gs = fig.add_gridspec(3, 1, hspace=0.10)

    w = s[s.material_type == "white"].sort_values("p", ascending=False).iloc[0]
    mark = w.date

    for i, mt in enumerate(["white", "green", "brown"]):
        ax = fig.add_subplot(gs[i])
        rahmen(ax)
        ax.axhspan(100, 110, color=C_UEBER, alpha=0.07, lw=0)
        ax.axhline(100, color=C_UEBER, lw=0.7, ls=(0, (4, 4)), alpha=0.5)
        e = s[s.material_type == mt].sort_values("date")
        y = np.where(e.ueber, 103.0, e.p)
        xs, ys = [], []
        for j in range(len(e)):
            xs += [e.date.iloc[j], e.date.iloc[j]]
            ys += [0.0, y[j]]
            if j + 1 < len(e):
                xs += [e.date.iloc[j], e.date.iloc[j + 1]]
                ys += [0.0, y[j + 1]]
        ax.plot(xs, ys, ls=":", lw=1.1, color=GLAS[mt][1], alpha=0.8, zorder=1)
        for k in MARKE:
            sel = (e.klasse == k).values
            if sel.any():
                ax.scatter(e.date[sel], (y if k != "passt" else e.p.values)[sel],
                           marker=MARKE[k], s=55, color=FARBE[k], edgecolor="white",
                           linewidth=0.8, zorder=3)
        ax.axvline(mark, color="#E8A33D", lw=6, alpha=0.22, zorder=0)
        ax.set_ylim(0, 110)
        ax.set_yticks([0, 50, 100])
        ax.tick_params(labelsize=10)
        ax.text(0.995, 0.90, f"{GLAS[mt][0]}  Ø {e.v.mean():.0f} %",
                transform=ax.transAxes, ha="right", va="top", fontsize=12.5,
                weight="bold", color=GLAS[mt][1],
                bbox=dict(fc="white", ec="none", alpha=0.85, pad=2.0))
        if i == 0:
            ax.text(0.004, 0.995, "≥ 100 % = overfull · Wert unbekannt",
                    transform=ax.transAxes, fontsize=9, color=C_UEBER, va="top")
            ax.annotate("derselbe Besuch",
                        xy=(mark, 101), xytext=(mark + pd.Timedelta(days=18), 42),
                        fontsize=10.5, color="#8A5A00",
                        bbox=dict(fc="white", ec="none", alpha=0.85, pad=2.0),
                        arrowprops=dict(arrowstyle="->", color="#8A5A00", lw=1.0,
                                        connectionstyle="arc3,rad=0.25"))
        if i == 2:
            monats_ticks(ax, d)
            ax.set_xlim(d.date.min() - pd.Timedelta(days=8), d.date.max() + pd.Timedelta(days=8))
            ax.set_xlabel("Messdatum (Tagesauflösung)", fontsize=10.5)
        else:
            ax.tick_params(labelbottom=False)
        if i == 1:
            ax.set_ylabel("Füllstand in %", fontsize=10.5)

    fig.savefig(OUT / "01_mechanismus.png")
    plt.close(fig)
    return lid


# ---------------------------------------------------------------- Bild 2 ----
def bild_alle(d):
    t = (d.groupby("Location_id")
           .agg(n=("v", "size"), mittel=("v", "mean"), median=("v", "median"),
                ueber=("ueber", "mean"))
           .sort_values(["median", "mittel"], ascending=False))
    t["rang"] = np.arange(len(t))

    fig = leinwand(
        "449 Orte, sortiert nach Füllstand — ohne Karte",
        "Jeder Strich ist ein Ort: sein Median-Füllstand bei der Ablesung. Der Punkt zeigt, wie oft er übervoll war.\n"
        "Die Reihenfolge ist keine Lage, sondern ein Datenwert. Kein Abstand, keine Route, keine Geografie.",
        f"Quelle: data/raw/glass_fill_levels_anonymized_f.csv · scripts/bilder.py · "
        f"{len(t)} Orte · 1.338 Container · 11.701 Messungen · overfull zählt als 100 %",
        top=0.80)
    ax = fig.add_subplot(111)
    rahmen(ax, achse="x")
    ax.barh(t.rang, t["median"], height=0.9, color="#C9CED6", lw=0, zorder=2)
    ax.scatter(t.ueber * 100, t.rang, s=6, color=C_UEBER, lw=0, zorder=3)
    ax.set_xlim(0, 100)
    ax.set_ylim(len(t), 0)
    ax.set_yticks([])
    ax.set_xlabel("Median-Füllstand dieses Ortes bei der Ablesung, in %", fontsize=11)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f} %"))
    med = t["median"].median()
    ax.axvline(med, color="#444444", lw=1.1, ls="--", zorder=4)
    ax.text(med + 1.2, len(t) * 0.5, f"Median aller Orte {med:.0f} %",
            rotation=90, va="center", ha="left", fontsize=10, color="#333333",
            bbox=dict(fc="white", ec="none", pad=1.5))
    ax.text(-0.008, 0.995, "fast immer voll", transform=ax.transAxes, rotation=90,
            ha="right", va="top", fontsize=10.5, color="#333333")
    ax.text(-0.008, 0.005, "fast immer leer angefahren", transform=ax.transAxes, rotation=90,
            ha="right", va="bottom", fontsize=10.5, color="#333333")
    leg = [Line2D([], [], marker="s", ls="", markersize=11, color="#C9CED6",
                  label="Median-Füllstand"),
           Line2D([], [], marker="o", ls="", markersize=7, color=C_UEBER,
                  label="Anteil overfull")]
    ax.legend(handles=leg, loc="lower right", frameon=True, framealpha=0.95,
              edgecolor="none", fontsize=10.5)

    fig.savefig(OUT / "02_alle_orte.png")
    plt.close(fig)


# ---------------------------------------------------------------- Bild 3 ----
def bild_einheit(d):
    links = (pd.crosstab(d.material_type, d.klasse)
               .reindex(columns=["zu frueh", "passt", "uebervoll"], fill_value=0)
               .reindex(["brown", "green", "white"]))
    v = (d.groupby(["Location_id", "date"]).v.max().rename("mx").reset_index())
    v["klasse"] = np.where(v.mx >= SCHWELLE_UEBER, "uebervoll",
                           np.where(v.mx < SCHWELLE_FRUEH, "zu frueh", "passt"))
    rechts = v.klasse.value_counts().reindex(["zu frueh", "passt", "uebervoll"])

    fig = leinwand(
        "Dieselben Daten, zwei Einheiten — und zwei verschiedene Geschichten",
        "Je Ablesung ist Braun fast immer unter 50 %. Je Besuch verschwindet das, weil ein Besuch drei\n"
        "Farben gleichzeitig trifft. Deshalb steht die Einheit neben jeder Zahl.",
        "Quelle: data/raw/glass_fill_levels_anonymized_f.csv · scripts/bilder.py · "
        "11.701 Ablesungen · 4.468 Besuche · Klassen sind Anzeige-Grenzen",
        top=0.78, left=0.115)
    gs = fig.add_gridspec(1, 2, width_ratios=[2.5, 1.3], wspace=0.10)
    ax1, ax2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

    for ax in (ax1, ax2):
        for s in ("top", "right", "left", "bottom"):
            ax.spines[s].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_ylim(-1.1, 2.6)

    for i, mt in enumerate(["brown", "green", "white"]):
        z = links.loc[mt]
        n = int(z.sum())
        x = 0.0
        for k in ["zu frueh", "passt", "uebervoll"]:
            a = z[k] / n
            ax1.barh(i, a, left=x, height=0.56, color=FARBE[k], edgecolor="white", lw=2)
            if a < 0.06:
                ax1.text(x + a / 2, i + 0.36, f"{a:.0%}", ha="center", va="bottom",
                         color=FARBE[k], fontsize=10.5, weight="bold")
            else:
                ax1.text(x + a / 2, i, f"{a:.0%}", ha="center", va="center",
                         color="white", fontsize=13.5, weight="bold")
            x += a
        ax1.text(-0.012, i, f"{GLAS[mt][0]}\n{zt(n)} Ablesungen", ha="right", va="center",
                 fontsize=12.5, weight="bold", color=GLAS[mt][1])
    ax1.set_xlim(0, 1)
    ax1.set_title("je Ablesung (Container + Farbe)", fontsize=13, loc="left", pad=12)

    n = int(rechts.sum())
    x = 0.0
    for k in ["zu frueh", "passt", "uebervoll"]:
        a = rechts[k] / n
        ax2.barh(1.0, a, left=x, height=0.56, color=FARBE[k], edgecolor="white", lw=2)
        x += a
    ax2.set_xlim(0, 1)
    ax2.text(0.0, 1.52, f"alle {zt(n)} Besuche", ha="left", va="bottom",
             fontsize=12.5, weight="bold")
    for j, k in enumerate(["zu frueh", "passt", "uebervoll"]):
        ax2.text(0.0, 0.52 - j * 0.30, f"{rechts[k] / n:.0%}  {KLASSE_TEXT[k]}",
                 ha="left", va="top", fontsize=11.5, color=FARBE[k])
    ax2.set_title("je Besuch (vollste Farbe)", fontsize=13, loc="left", pad=12)

    leg = [Line2D([], [], marker="s", ls="", markersize=13, color=FARBE[k],
                  label=KLASSE_TEXT[k]) for k in FARBE]
    fig.legend(handles=leg, loc="lower left", bbox_to_anchor=(0.115, 0.055),
               frameon=False, fontsize=11, ncol=3)

    fig.savefig(OUT / "03_einheit.png")
    plt.close(fig)


# ---------------------------------------------------------------- Bild 4 ----
def bild_takt(d):
    x = d.sort_values(["Location_id", "material_type", "date"]).copy()
    x["abstand"] = x.groupby(["Location_id", "material_type"]).date.diff().dt.days
    x = x.dropna(subset=["abstand"])
    x["klasse"] = pd.cut(x.abstand, [0, 7, 14, 30, 60, 400],
                         labels=["≤ 7 Tage", "8–14 Tage", "15–30 Tage", "31–60 Tage", "> 60 Tage"])
    t = x.groupby("klasse", observed=True).agg(n=("p", "size"), mittel=("p", "mean"),
                                               ueber=("ueber", "mean"))

    fig = leinwand(
        "Länger warten füllt nicht mehr — aber es läuft über",
        "Abstand seit der letzten Leerung, gegen den Füllstand bei der nächsten Ablesung.\n"
        "Der Mittelwert ist ohne overfull gerechnet, deshalb wird er flach. Der Überlauf steigt weiter.",
        "Quelle: data/raw/glass_fill_levels_anonymized_f.csv · scripts/bilder.py · "
        f"{zt(int(t.n.sum()))} Ablesungen mit bekanntem Vorgänger · 1.338 Container",
        top=0.78, bottom=0.13)
    gs = fig.add_gridspec(2, 1, height_ratios=[2.1, 1.0], hspace=0.22)
    ax1, ax2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1], sharex=None)

    xs = np.arange(len(t))
    rahmen(ax1)
    ax1.bar(xs, t.mittel, width=0.52, color="#C9CED6", lw=0, zorder=2)
    for i, v in enumerate(t.mittel):
        ax1.text(i, v + 2, f"{v:.0f} %", ha="center", va="bottom", fontsize=14, weight="bold")
    ax1.set_ylim(0, 100)
    ax1.set_yticks([0, 25, 50, 75, 100])
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f} %"))
    ax1.tick_params(labelbottom=False, labelsize=11)
    ax1.set_ylabel("Füllstand bei der Ablesung\nMittel in % (ohne overfull)", fontsize=11)
    ax1.set_title("Füllstand", fontsize=12, loc="left", pad=8, color="#555555")

    rahmen(ax2)
    ax2.plot(xs, t.ueber * 100, color=C_UEBER, lw=2.4, marker="o", ms=10,
             mfc="white", mew=2.2, zorder=3)
    for i, v in enumerate(t.ueber * 100):
        ax2.text(i, v + 0.9, f"{v:.1f} %".replace(".", ","), ha="center", va="bottom",
                 fontsize=12, color=C_UEBER, weight="bold")
    ax2.set_ylim(0, 22)
    ax2.set_yticks([0, 5, 10, 15, 20])
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f} %"))
    ax2.tick_params(labelsize=11)
    ax2.set_ylabel("Anteil overfull", fontsize=11, color=C_UEBER)
    ax2.set_title("Überlauf bei der Ablesung", fontsize=12, loc="left", pad=8, color=C_UEBER)
    ax2.set_xticks(xs)
    ax2.set_xticklabels([f"{i}\nn = {zt(n)}" for i, n in zip(t.index, t.n)], fontsize=11.5)
    ax2.set_xlabel("Abstand seit der letzten Leerung", fontsize=11, labelpad=8)
    ax2.set_xlim(-0.6, len(t) - 0.4)

    fig.savefig(OUT / "04_takt.png")
    plt.close(fig)
    return t


def main():
    d = lade()
    lid = bild_mechanismus(d)
    bild_alle(d)
    bild_einheit(d)
    t = bild_takt(d)
    print("Beispielort:", lid)
    print(t.round(3).to_string())
    for p in sorted(OUT.glob("*.png")):
        print(f"{p.relative_to(ROOT)}  {p.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
