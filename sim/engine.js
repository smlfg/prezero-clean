/* Simulations-Engine - reine Logik, ohne DOM.
   Identisch zu scripts/sim_referenz.py (siehe docs/KINO_VERTRAG.md).
   Verwendung:
     Browser: window.KINO.create(daten)
     Node:    const KINO = require('./sim/engine.js'); KINO.create(daten)
*/
var KINO = (function () {
  "use strict";

  var K0 = 12.8;        // Stopps/Tag im Ist-Durchsatz
  var S0 = 5.0;         // Abstandseinheiten im Ist-Fall
  var WARMLAUF = 90;    // Tage ohne Zaehlung
  var VOLL = 100.0;     // >= 100 % gilt als voll/uebervoll
  var MAXC = 3;

  function create(daten) {
    var META = daten.meta;
    var orte = daten.orte;
    var N = orte.length;
    var TAGE = META.tage;

    var rate = new Float64Array(N * MAXC);
    var anz = new Int32Array(N);
    var periode = new Float64Array(N);
    var ids = new Array(N);
    var FAKTOR = META.kalibrierungsfaktor;

    for (var i = 0; i < N; i++) {
      var o = orte[i];
      ids[i] = o.id;
      anz[i] = o.container.length;
      for (var j = 0; j < o.container.length; j++) {
        var r = o.container[j].rate;
        rate[i * MAXC + j] = (r === null || r === undefined) ? 0 : r;
      }
      periode[i] = (o.gap === null || o.gap === undefined) ? TAGE : o.gap * FAKTOR;
    }

    var P = { s: 5.0, m: 1, strategie: "ist", schwelle: 80 };
    var fill, naechste, budget, tag, leerungen, ueberlaufTage, vollBeiLeerung,
        ueber100, maxSumme, faelligSumme, fuellSumme, fuellZaehler, tagesverlauf,
        autos, letzteTage, maxfill;

    function reset(p) {
      if (p) {
        if (p.s !== undefined) P.s = p.s;
        if (p.m !== undefined) P.m = p.m;
        if (p.strategie !== undefined) P.strategie = p.strategie;
        if (p.schwelle !== undefined) P.schwelle = p.schwelle;
      }
      fill = new Float64Array(N * MAXC);
      maxfill = new Float64Array(N);
      naechste = new Float64Array(N);
      budget = 0; tag = 0; leerungen = 0; ueberlaufTage = 0; vollBeiLeerung = 0;
      ueber100 = 0; maxSumme = 0; faelligSumme = 0; fuellSumme = 0; fuellZaehler = 0;
      tagesverlauf = []; letzteTage = [];
      for (var i = 0; i < N; i++) naechste[i] = i * periode[i] / N;
      autos = [];
      for (var k = 0; k < P.m; k++) autos.push({ pos: 0, weg: [] });
      /* Warmlauf sofort hinterziehen: er zaehlt nichts, erzeugt aber den realistischen
         Startzustand (gefuellte Puffer, bereits geleerte Orte). */
      while (tag < WARMLAUF) stepDay();
      return api;
    }

    function stepDay() {
      var i, j, mx;
      for (i = 0; i < N; i++) {
        mx = 0;
        for (j = 0; j < anz[i]; j++) {
          var idx = i * MAXC + j;
          fill[idx] += rate[idx];
          if (fill[idx] > mx) mx = fill[idx];
        }
        maxfill[i] = mx;
      }
      var messfenster = tag >= WARMLAUF;
      var faellig = [];
      for (i = 0; i < N; i++) {
        var due = P.strategie === "ist" ? tag >= naechste[i] : maxfill[i] >= P.schwelle;
        if (due) faellig.push(i);
      }
      if (messfenster) {
        for (i = 0; i < N; i++) if (maxfill[i] >= VOLL) ueberlaufTage++;
        for (i = 0; i < N; i++) {
          for (j = 0; j < anz[i]; j++) {
            var v = fill[i * MAXC + j];
            if (v <= VOLL) { fuellSumme += v; fuellZaehler++; }
          }
        }
        faelligSumme += faellig.length;
      }
      budget += P.m * K0 * S0 / P.s;
      var bedient = [];
      if (faellig.length) {
        faellig.sort(function (a, b) {
          var d = maxfill[b] - maxfill[a];
          if (d) return d;
          return ids[a] < ids[b] ? -1 : 1;
        });
        for (var q = 0; q < faellig.length; q++) {
          if (budget < 1) break;
          budget -= 1;
          i = faellig[q];
          for (j = 0; j < anz[i]; j++) fill[i * MAXC + j] = 0;
          if (P.strategie === "ist") naechste[i] = tag + periode[i];
          if (messfenster) {
            leerungen++;
            maxSumme += Math.min(VOLL, maxfill[i]);
            if (maxfill[i] >= VOLL) vollBeiLeerung++;
            if (maxfill[i] > VOLL) ueber100++;
          }
          bedient.push(i);
        }
      }
      for (var k2 = 0; k2 < autos.length; k2++) autos[k2].weg = [];
      for (var b = 0; b < bedient.length; b++) autos[b % autos.length].weg.push(bedient[b]);
      if (messfenster) {
        tagesverlauf.push({ tag: tag - WARMLAUF + 1, ueberlauf: ueberlaufTage, leerungen: leerungen });
      }
      letzteTage = bedient;
      tag++;
      return bedient.length;
    }

    function metrics() {
      var t = Math.max(1, TAGE);
      return {
        tag: Math.max(0, tag - WARMLAUF),
        leerungen: leerungen,
        ueberlauf_tage: ueberlaufTage,
        ueberlauf_quote_pct: +(100 * ueberlaufTage / (N * t)).toFixed(2),
        voll_bei_leerung_pct: leerungen ? +(100 * vollBeiLeerung / leerungen).toFixed(2) : 0,
        ueber_100_bei_leerung_pct: leerungen ? +(100 * ueber100 / leerungen).toFixed(2) : 0,
        mittel_max_bei_leerung_pct: leerungen ? +(maxSumme / leerungen).toFixed(2) : 0,
        fuell_mittel: fuellZaehler ? +(fuellSumme / fuellZaehler).toFixed(2) : 0,
        wegeinheiten: +(P.s * leerungen).toFixed(1),
        auslastung_pct: faelligSumme ? +(100 * leerungen / faelligSumme).toFixed(2) : 0,
        stopps_pro_tag: +(leerungen / t).toFixed(3),
        soll_stopps_pro_tag: +(P.m * K0 * S0 / P.s).toFixed(3),
        kalibrierungsfaktor: FAKTOR
      };
    }

    function runToEnd() {
      while (tag < WARMLAUF + TAGE) stepDay();
      return metrics();
    }

    var api = {
      meta: META, n: N, tage: TAGE, warmlauf: WARMLAUF, ids: ids,
      setParams: function (p) { Object.assign(P, p); return api; },
      getParams: function () { return { s: P.s, m: P.m, strategie: P.strategie, schwelle: P.schwelle }; },
      reset: reset, stepDay: stepDay, metrics: metrics, runToEnd: runToEnd,
      get fill() { return fill; },
      get maxfill() { return maxfill; },
      get anz() { return anz; },
      get tag() { return tag; },
      get autos() { return autos; },
      get letzteTage() { return letzteTage; },
      get tagesverlauf() { return tagesverlauf; }
    };
    return reset(null);
  }

  return { create: create, K0: K0, S0: S0, WARMLAUF: WARMLAUF, VOLL: VOLL, MAXC: MAXC };
})();

if (typeof module !== "undefined" && module.exports) module.exports = KINO;
