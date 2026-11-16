/* Prueft die JavaScript-Engine (sim/engine.js) gegen die Python-Referenz
   (scripts/sim_referenz.py). Beide sind unabhaengig nach docs/KINO_VERTRAG.md gebaut.

   Aufruf:  node scripts/sim_check.js
             node scripts/sim_check.js --json
*/
"use strict";
const fs = require("fs");
const path = require("path");
const KINO = require(path.join(__dirname, "..", "sim", "engine.js"));

const ROOT = path.join(__dirname, "..");
const DATEN = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "derived", "orte.json"), "utf8"));

const LAEUFE = [
  { name: "default", s: 5, m: 1, strategie: "ist", schwelle: 80 },
  { name: "s10", s: 10, m: 1, strategie: "ist", schwelle: 80 },
  { name: "s20", s: 20, m: 1, strategie: "ist", schwelle: 80 },
  { name: "m4_ist", s: 5, m: 4, strategie: "ist", schwelle: 80 },
  { name: "m4_fuell", s: 5, m: 4, strategie: "fuell", schwelle: 80 }
];

const out = {};
for (const l of LAEUFE) {
  const eng = KINO.create(DATEN);
  eng.setParams({ s: l.s, m: l.m, strategie: l.strategie, schwelle: l.schwelle });
  eng.reset();
  out[l.name] = eng.runToEnd();
}

if (process.argv.includes("--json")) {
  console.log(JSON.stringify(out, null, 1));
} else {
  console.log("JavaScript-Engine (sim/engine.js), Läufe über das ganze Fenster:");
  for (const l of LAEUFE) {
    const m = out[l.name];
    console.log(`\n${l.name}  (s=${l.s} m=${l.m} ${l.strategie}${l.strategie === "fuell" ? "@" + l.schwelle : ""})`);
    console.log(`  Leerungen: ${m.leerungen} | Stopps/Tag: ${m.stopps_pro_tag} / Soll ${m.soll_stopps_pro_tag}`);
    console.log(`  Überlauf-Tage: ${m.ueberlauf_tage} | voll/übervoll b. Leerung: ${m.voll_bei_leerung_pct} %` +
                ` | > 100 %: ${m.ueber_100_bei_leerung_pct} %`);
    console.log(`  mittlere vollste Kammer: ${m.mittel_max_bei_leerung_pct} % | Ø Füllstand: ${m.fuell_mittel} %` +
                ` | Wegeinheiten: ${m.wegeinheiten} | Auslastung: ${m.auslastung_pct} %`);
  }
}
