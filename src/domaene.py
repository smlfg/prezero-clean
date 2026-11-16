"""Domänenmodell `Glas` – `Container` – `LKW` nach AGENTS.md §2.

Drei Objekte, zwei getrennte Mengen (AGENTS.md §2, LKW-Zeile):

1. **Glas (Inhalt):** Farbe ∈ {braun, weiß, grün} (`brown`, `green`, `white`),
   Menge in % der Kammer. Füllstand 0–100 %, `overfull` = Überlauf (rechtszensiert, A3).
2. **Container (Puffer):** `Location_id` (449) mit Kammern je Farbe. Ein Container
   hat 1–3 Kammern (441×3, 7×2, 1×1 -> 1.338 Kammern).
3. **LKW (Consumer):** `besuch(datum, location_id)`:
   - **misst** eine Teilmenge der Kammern (296 Besuche mit 1 Farbe, 1.111 mit 2,
     3.061 mit 3 -> nur 3.075 Besuche messen alle Kammern des Containers),
   - **leert** alle Kammern des Containers auf 0 (A1, gesetzte Annahme).

Wichtig: Messen und Leeren sind zwei verschiedene Mengen. Der Messwert ist der
Füllstand **vor** der Leerung (A5). Die CSV enthält keinen Stand nach dem Besuch.

Erlaubte Spalten der Quelle: `Location_id`, `material_type`, `date`, `fill_level_perc`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "raw" / "glass_fill_levels_anonymized_f.csv"
ERLAUBTE_SPALTEN = ["Location_id", "material_type", "date", "fill_level_perc"]

FARBEN = ("brown", "green", "white")
Ueberfull = "overfull"


@dataclass(frozen=True)
class Glas:
    """Inhalt einer Kammer: eine Farbe und ihre Menge in % der Kammer.

    `menge` ist der Füllstand 0..100 %. Oberhalb von 100 % ist der Wert unbekannt
    (rechtszensiert, A3) und wird als `overfull` abgebildet.
    """

    farbe: str
    menge: float = 0.0

    def __post_init__(self) -> None:
        if self.farbe not in FARBEN:
            raise ValueError(f"unbekannte Glasfarbe: {self.farbe!r} (erlaubt: {FARBEN})")

    @property
    def uebervoll(self) -> bool:
        """True, wenn die Menge die Kammergrenze 100 % übersteigt (A3)."""
        return self.menge > 100.0

    def ablesen(self) -> float | str:
        """Skalenwert der Messung: 10er-Stufe 0..100 oder 'overfull' (A3)."""
        if self.uebervoll:
            return Ueberfull
        return float(self.menge)

    def __add__(self, other: Glas) -> Glas:
        if not isinstance(other, Glas) or other.farbe != self.farbe:
            raise TypeError("Glas addiert sich nur mit derselben Farbe")
        return Glas(self.farbe, self.menge + other.menge)


@dataclass
class Kammer:
    """Eine Farb-Kammer im Container: Inhalt (`Glas`) plus Zustand."""

    farbe: str
    fuellstand: float = 0.0

    def fuellen(self, menge: float) -> None:
        """Zufluss (A2): die Menge wächst um `menge` Prozentpunkte."""
        self.fuellstand += menge

    def leeren(self) -> None:
        """Leerung (A1/A4): der Puffer steht danach wieder auf 0 %."""
        self.fuellstand = 0.0

    def ablesen(self) -> float | str:
        """Skalenwert der Messung: 10er-Stufe 0..100 oder 'overfull' (A3)."""
        return Glas(self.farbe, self.fuellstand).ablesen()

    def glas(self) -> Glas:
        return Glas(self.farbe, self.fuellstand)


@dataclass
class Container:
    """Container (Puffer) an einem Standort: 1–3 Kammern je Farbe.

    Schlüssel: `Location_id` (449 Container). Die Kammerzahl folgt aus den
    Daten: 441 mit drei Farben, 7 mit zwei, 1 mit einer.
    """

    location_id: str
    kammern: dict[str, Kammer] = field(default_factory=dict)

    @classmethod
    def aus_messungen(cls, location_id: str, farben: list[str]) -> Container:
        return cls(location_id=location_id, kammern={f: Kammer(f) for f in farben})

    def fuellen_bis(self, tage: float, raten: dict[str, float]) -> None:
        """Integriert den Zufluss über `tage` Tage (A2): Füllrate je Farbe in %/Tag."""
        for farbe, kammer in self.kammern.items():
            kammer.fuellen(raten.get(farbe, 0.0) * tage)

    def messen(self) -> dict[str, float | str]:
        """Liest alle Kammern ab (Messwert = Stand **vor** der Leerung, A5)."""
        return {f: k.ablesen() for f, k in self.kammern.items()}

    def leeren(self) -> None:
        """Leert **alle** Kammern des Containers auf 0 (A1)."""
        for kammer in self.kammern.values():
            kammer.leeren()

    @property
    def max_fuellstand(self) -> float:
        return max((k.fuellstand for k in self.kammern.values()), default=0.0)


@dataclass
class Besuch:
    """Ein LKW-Besuch an einem Standort an einem Kalendertag.

    Schlüssel: (`Location_id`, `date`). `gemessen` sind die Kammern, die der
    Fahrer tatsächlich abgelesen hat; `geleert` sind die Kammern, die auf 0
    gesetzt wurden (A1: alle).
    """

    location_id: str
    datum: pd.Timestamp
    gemessen: frozenset[str] = frozenset()
    geleert: frozenset[str] = frozenset()


@dataclass
class LKW:
    """Der Consumer: fährt Standorte an, misst eine Teilmenge, leert alles (A1)."""

    besuche: list[Besuch] = field(default_factory=list)

    def besuchen(self, container: Container, datum: pd.Timestamp) -> Besuch:
        """Misiert die Kammern des Containers und leert danach alle (A1, A5).

        Der gemessene Füllstand ist der Stand **vor** der Leerung (A5).
        """
        abgelesen = container.messen()
        gemessen = frozenset(abgelesen)
        container.leeren()
        besuch = Besuch(
            location_id=container.location_id,
            datum=pd.Timestamp(datum),
            gemessen=gemessen,
            geleert=frozenset(container.kammern),
        )
        self.besuche.append(besuch)
        return besuch


def lade_messungen(csv_pfad: str | Path = DEFAULT_CSV) -> pd.DataFrame:
    """Lädt die Rohdaten (nur die 4 erlaubten Spalten) mit Besuchs-/Messabständen.

    Spalten:
      - `ueber`: True bei Textwert 'overfull' (rechtszensiert, A3).
      - `p`: numerischer Füllstand (NaN bei 'overfull').
      - `p_untergrenze`: 100.0 bei 'overfull', sonst `p`.
      - `abstand_ort`: Tage bis zum vorigen Besuch desselben Standorts (A1).
      - `abstand`: Tage bis zur vorigen Messung derselben Kammer (A4).
    """
    raw = pd.read_csv(csv_pfad, usecols=ERLAUBTE_SPALTEN, parse_dates=["date"])
    d = raw[ERLAUBTE_SPALTEN].copy()
    d["ueber"] = d["fill_level_perc"].eq(Ueberfull)
    d["p"] = pd.to_numeric(d["fill_level_perc"].where(~d["ueber"]))
    d["p_untergrenze"] = np.where(d["ueber"], 100.0, d["p"])

    v = d[["Location_id", "date"]].drop_duplicates().sort_values(["Location_id", "date"])
    v["abstand_ort"] = v.groupby("Location_id")["date"].diff().dt.days
    d = d.merge(v, on=["Location_id", "date"], how="left")

    d = d.sort_values(["Location_id", "material_type", "date"]).reset_index(drop=True)
    d["abstand"] = d.groupby(["Location_id", "material_type"])["date"].diff().dt.days
    return d


def baue_container(df: pd.DataFrame) -> dict[str, Container]:
    """Baut je Standort einen Container mit seinen Kammern (aus den Daten)."""
    container: dict[str, Container] = {}
    for lid, sub in df.groupby("Location_id", sort=True):
        container[lid] = Container.aus_messungen(lid, sorted(sub["material_type"].unique()))
    return container


def baue_besuche(df: pd.DataFrame) -> list[Besuch]:
    """Baut die Besuche (LKW-Ereignisse) aus der CSV.

    `gemessen` = tatsächlich abgelesene Kammern. `geleert` = **alle** Kammern des
    Containers (A1), auch die ungemessenen. Bei 1.393 Besuchen wurde nur eine
    Teilmenge gemessen (AGENTS.md §2); die CSV entscheidet nicht, ob die
    ungemessenen Kammern tatsächlich geleert wurden — A1 bleibt gesetzte Annahme.
    """
    kammern_je_id = df.groupby("Location_id")["material_type"].apply(
        lambda s: frozenset(s.unique())
    )
    besuche: list[Besuch] = []
    for (lid, datum), sub in df.groupby(["Location_id", "date"], sort=True):
        besuche.append(
            Besuch(
                location_id=lid,
                datum=pd.Timestamp(datum),
                gemessen=frozenset(sub["material_type"].unique()),
                geleert=kammern_je_id[lid],
            )
        )
    return besuche


def domaene_kennzahlen(df: pd.DataFrame) -> dict[str, int | float]:
    """Mengengerüst des Domänenmodells (alle Zahlen aus der CSV).

    Enthält die Trennung von Messen und Leeren: `besuche_messen_alle_kammern`
    ist kleiner als `besuche` gesamt.
    """
    kammern_je_id = df.groupby("Location_id")["material_type"].nunique()
    v = df.groupby(["Location_id", "date"]).agg(
        farben_gemessen=("material_type", "nunique")
    ).reset_index()
    v = v.merge(kammern_je_id.rename("kammern"), on="Location_id")
    v["voll"] = v["farben_gemessen"] == v["kammern"]

    return {
        "container": int(df["Location_id"].nunique()),
        "kammern": int(df.groupby(["Location_id", "material_type"]).ngroups),
        "messungen": len(df),
        "besuche": len(v),
        "besuche_messen_alle_kammern": int(v["voll"].sum()),
        "besuche_messen_teilmenge": int((~v["voll"]).sum()),
        "kammern_je_container": kammern_je_id.value_counts().sort_index().to_dict(),
        "ueberlauf_messungen": int(df["ueber"].sum()),
    }
