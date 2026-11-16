/* Regression: changing the distance parameter at reset must not change Tag 0.
   Run with: node tests/test_sim_day0.js */
"use strict";

const assert = require("assert");
const KINO = require("../sim/engine.js");

const daten = {
  meta: { tage: 10, k0_pro_tag: 1, s0: 5, kalibrierungsfaktor: 1 },
  orte: [
    { id: "a", gap: 2, container: [{ rate: 10 }, { rate: 5 }] },
    { id: "b", gap: 4, container: [{ rate: 8 }, { rate: 4 }] },
    { id: "c", gap: 6, container: [{ rate: 6 }, { rate: 3 }] },
  ],
};

function resetAt(distance) {
  const engine = KINO.create(daten);
  engine.setParams({ s: distance });
  engine.reset();
  return { tag: engine.tag, fill: Array.from(engine.fill) };
}

const atFive = resetAt(5);
const atTen = resetAt(10);
assert.strictEqual(atFive.tag, 0, "reset muss bei Tag 0 bleiben");
assert.strictEqual(atTen.tag, 0, "reset muss bei Tag 0 bleiben");
assert.deepStrictEqual(
  atFive.fill,
  atTen.fill,
  "der Abstand darf den Füllstand vor dem ersten Zeitschritt nicht ändern"
);

console.log("ok: Tag 0 bleibt beim Ändern des Abstands unverändert");
