#!/usr/bin/env python3
"""Vorschau-Bilder der LKW-Objekte fuer das Drehbuch.

Aufruf: python scripts/bilder_lkw.py
Ausgabe in bilder/lkw/:
  gc23.png  x4h.png  hakenlift.png  presse20.png  arkm36.png

Eine Aussage je Bild: "so viele PreZero-Standorte passen auf dieses LKW".

Links die Seitenansicht des LKW, massstaeblich (Aufbauvolumen proportional zum
Ladevolumen). Rechts der Massbalken: Ladevolumen gegen einen vollen PreZero-Standort
(6,4 m3, A6/V-3) und gegen die beobachtete Ladung je Besuch (Median, obere Schranke).

Keine Karte, keine Euro, keine km, keine Tonnen - diese Groessen stehen in keiner
Quelle. Die Ladevolumina sind recherchiert (docs/externe_parameter.md V-5), nicht
gemessen und nicht modelliert. Das LKW ist ein PLATZHALTER: es aendert den Lauf nicht.

Regeln: assets/ui/UI_REGELN.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lkw_katalog import (  # noqa: E402
    ABRUF,
    LADUNG_MEDIAN_M3,
    LKW,
    PLATZHALTER_TEXT,
    STANDORT_VOLL_M3,
    orte_je_tour,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "bilder" / "lkw"

C_LKW = "#2F4A6D"
C_LKW_HELL = "#7C96B5"
C_STANDORT = "#B3261E"
C_LADUNG = "#E8A33D"
C_TEXT = "#222222"
C_MUTED = "#666666"
C_GRAU = "#E8E8E8"


def leinwand(titel, unter, quelle):
    fig = plt.figure(figsize=(16, 9), dpi=100)
    fig.text(0.012, 0.975, titel, fontsize=19, weight="bold", ha="left", va="top")
    fig.text(0.012, 0.925, unter, fontsize=12.2, color=C_TEXT, ha="left", va="top",
             linespacing=1.45)
    fig.text(0.012, 0.016, quelle, fontsize=8.6, color=C_MUTED, ha="left", va="bottom",
             linespacing=1.5)
    fig.subplots_adjust(left=0.045, right=0.975, top=0.80, bottom=0.145)
    return fig


def zeichne_lkw(ax, obj):
    """Seitenansicht: Fahrerhaus + Aufbau, massstaeblich in Metern."""
    L = obj["laenge_m"]
    H = obj["hoehe_m"]
    B = obj["breite_m"]

    # Aufbau: Laenge des Aufbaus proportional zum Ladevolumen.
    # Bezug: der groesste Katalogwert = 36 m3 -> 6,4 m Aufbau.
    anteil = obj["volumen_m3"] / 36.0
    aufbau_l = max(2.0, 6.4 * anteil)
    kabine_l = max(1.8, L - aufbau_l)

    rad = 0.52
    # Fahrgestell
    ax.add_patch(Rectangle((0, rad), L, 0.34, facecolor="#3A3A3A",
                           edgecolor="none", zorder=2))
    # Aufbau (Ladekoerper)
    ax.add_patch(Rectangle((kabine_l, rad + 0.34), aufbau_l, H - rad - 0.34,
                           facecolor=C_LKW, edgecolor=C_LKW, lw=1.6, zorder=3))
    # Fahrerhaus
    kab_h = H - rad - 0.34
    ax.add_patch(Rectangle((0, rad + 0.34), kabine_l, kab_h, facecolor=C_LKW_HELL,
                           edgecolor=C_LKW, lw=1.6, zorder=3))
    # Fenster der Kabine
    if kabine_l > 1.6:
        ax.add_patch(Rectangle((kabine_l * 0.50, rad + 0.34 + kab_h - 0.85),
                               kabine_l * 0.34, 0.55,
                               facecolor="white", edgecolor=C_LKW, lw=1.0, zorder=4))
    # Raeder
    for x in (kabine_l * 0.32, kabine_l + aufbau_l * 0.74):
        ax.add_patch(plt.Circle((x, rad), rad, facecolor="#3A3A3A", edgecolor="white",
                                lw=1.4, zorder=5))
        ax.add_patch(plt.Circle((x, rad), rad * 0.42, facecolor="#B8B8B8",
                                edgecolor="none", zorder=6))

    # Masslinie mit Laenge in Metern
    y = -0.55
    ax.annotate("", xy=(0, y), xytext=(L, y),
                arrowprops=dict(arrowstyle="<->", color=C_MUTED, lw=1.0))
    ax.text(L / 2, y - 0.42, f"{L:.1f} m", fontsize=10.5, color=C_MUTED, ha="center")

    # Hoehenmass an der Aufbau-Schnittkante
    x0 = kabine_l + aufbau_l
    ax.annotate("", xy=(x0 + 0.30, 0), xytext=(x0 + 0.30, H),
                arrowprops=dict(arrowstyle="<->", color=C_MUTED, lw=1.0))
    ax.text(x0 + 0.44, H * 0.72, f"{H:.1f} m hoch", fontsize=10.5, color=C_MUTED,
            va="center")
    ax.text(x0 + 0.44, H * 0.52, f"{B:.2f} m breit", fontsize=10.5, color=C_MUTED,
            va="center")

    ax.set_xlim(-0.6, L + 1.7)
    ax.set_ylim(-1.6, H + 1.2)
    ax.set_aspect("equal")
    ax.axis("off")


def zeichne_balken(ax, obj):
    """Massbalken: Ladevolumen gegen Standort und beobachtete Ladung."""
    v = obj["volumen_m3"]
    werte = [
        ("Ladevolumen dieses LKW", v, C_LKW),
        (f"1 voller PreZero-Standort (100 %)", STANDORT_VOLL_M3, C_STANDORT),
        ("beobachtete Ladung je Besuch (Median)", LADUNG_MEDIAN_M3, C_LADUNG),
    ]
    max_v = max(v, STANDORT_VOLL_M3) * 1.22

    y = np.arange(len(werte))[::-1]
    for yi, (label, wert, farbe) in zip(y, werte):
        ax.barh(yi, wert, height=0.5, color=farbe, zorder=3)
        ax.text(wert + max_v * 0.015, yi, f"{wert:.1f} m³", fontsize=12.5,
                weight="bold", va="center", color=C_TEXT, zorder=4)

    ax.set_yticks(y)
    ax.set_yticklabels([w[0] for w in werte], fontsize=11.5, ha="right")
    ax.set_xlim(0, max_v)
    ax.set_ylim(-0.55, len(werte) - 0.35)
    ax.set_xlabel("Kubikmeter", fontsize=11, color=C_MUTED, labelpad=6)
    ax.grid(axis="x", color=C_GRAU, lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10)

    # Aussage unter dem Balken, im freien Bereich der Achse.
    n = orte_je_tour(v)
    ax.text(0.0, -0.13,
            f"Das LKW fasst rechnerisch {n:.1f} × die beobachtete Ladung",
            transform=ax.transAxes, fontsize=12.5, weight="bold",
            color=C_TEXT, va="top")
    ax.text(0.0, -0.225,
            f"je Besuch ({LADUNG_MEDIAN_M3:.2f} m³). Die Daten zeigen trotzdem einen",
            transform=ax.transAxes, fontsize=11.5, color=C_MUTED, va="top")
    ax.text(0.0, -0.305,
            "Besuch je Ort — die Ladung ist balanciert.",
            transform=ax.transAxes, fontsize=11.5, color=C_MUTED, va="top")


def bild(obj):
    v = obj["volumen_m3"]
    n = orte_je_tour(v)
    fig = leinwand(
        f"{obj['name']} — {obj['volumen_text']} Ladevolumen",
        f"{obj['hersteller']} · {obj['typ']} · {obj['beschreibung']}\n"
        f"Das LKW fasst rechnerisch {n:.1f} Standorte je Tour. "
        f"Ein PreZero-Standort fasst bei 100 % {STANDORT_VOLL_M3:.1f} m³ "
        f"(weiß {3.2:.1f} + grün {2.1:.1f} + braun {1.1:.1f}, A6/V-3).",
        f"Recherchiert, Abrufdatum {ABRUF}: {obj['quelle']}\n"
        f"Referenzen: {LADUNG_MEDIAN_M3:.2f} m³ beobachtete Ladung je Besuch "
        f"(4.468 Besuche, obere Schranke) · {STANDORT_VOLL_M3:.1f} m³ Standort (A6/V-3) · "
        f"scripts/bilder_lkw.py · {PLATZHALTER_TEXT}",
        )
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.15], wspace=0.42)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    zeichne_lkw(ax1, obj)
    ax1.set_title(obj["typ"], fontsize=13, weight="bold", color=C_TEXT, loc="left", pad=8)
    ax1.text(0.0, -0.08,
             "Seitenansicht, schematisch · Maße aus der Herstellerangabe",
             transform=ax1.transAxes, fontsize=10, color=C_MUTED, va="top")

    zeichne_balken(ax2, obj)
    ax2.set_title("Ladevolumen im Maßstab", fontsize=13, weight="bold", color=C_TEXT,
                   loc="left", pad=8)

    OUT.mkdir(parents=True, exist_ok=True)
    ziel = OUT / f"{obj['id']}.png"
    fig.savefig(ziel, dpi=100)
    plt.close(fig)
    return ziel


def main() -> None:
    print(f"Vorschau-Bilder der LKW-Objekte (recherchiert, Abrufdatum {ABRUF})")
    print(f"Ausgabe: {OUT.relative_to(ROOT)}/")
    print()
    for obj in LKW:
        ziel = bild(obj)
        print(f"  {ziel.name:<16} {obj['name']:<32} {obj['volumen_text']:>10}")
    print()
    print(f"Hinweis: {PLATZHALTER_TEXT}")


if __name__ == "__main__":
    import numpy as np  # noqa: E402  (erst hier, damit der Import nicht unnoetig frueh fehlschlaegt)
    main()
