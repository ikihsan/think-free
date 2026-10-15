#!/usr/bin/env node
// Gate table for E162, computed from the recorded run files. Declared gates
// only: every threshold below is the one written in PROTOCOL.md before any
// page was fetched.
const fs = require("fs");
const path = require("path");
const H = require("./lib/harness");

const AA = new Set(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]);
const read = (f) => JSON.parse(fs.readFileSync(path.join(H.HERE, f), "utf8"));

function totals(rows) {
  const ok = rows.filter((r) => !r.error);
  const s = (k) => ok.reduce((a, r) => a + (r[k] || 0), 0);
  return { rows: ok, count: ok.length, s };
}

function armRow(label, policy, rows) {
  const { rows: ok, count, s } = totals(rows);
  const beforeAA = s("before_aa"), afterAA = s("after_aa");
  const applied = s("repairs_applied"), fab = s("repairs_fabricated");
  const elim = s("eliminated"), intro = s("introduced");
  const frames = {};
  for (const r of ok) {
    const f = frames[r.frame] || (frames[r.frame] = { eliminated: 0, introduced: 0 });
    f.eliminated += r.eliminated; f.introduced += r.introduced;
  }
  return {
    arm: label, policy, pages: count,
    before_total: s("before_total"), after_total: s("after_total"),
    before_aa: beforeAA, after_aa: afterAA,
    eliminated: elim, introduced: intro,
    aa_eliminated: Math.max(0, beforeAA - afterAA),
    aa_share_eliminated: beforeAA ? Math.max(0, beforeAA - afterAA) / beforeAA : null,
    repairs_applied: applied, repairs_fabricated: fab,
    fabrication_rate: applied ? fab / applied : null,
    pages_with_repair: ok.filter((r) => r.repairs_applied > 0).length,
    frames,
  };
}

function main() {
  // argv: [runLabel] -> results-<run>armA.json / results-<run>armB.json,
  // gates written to gates-<run>.json. Default "" = the canonical run 2.
  const run = process.argv[2] || "";
  const pre = run ? `results-${run}-` : "results-";
  const armAFile = `${pre}armA.json`;
  const armBFile = `${pre}armB.json`;
  const arm0 = read("results-arm0.json");
  const A = armRow("A", "blanket", read(armAFile).pages);
  const B = armRow("B", "conservative", read(armBFile).pages);
  const pagesMeasured = arm0.pages.length;
  const withViol = arm0.summary.pages_with_at_least_one_violation;

  // G0
  const g0 = {
    gate: "G0 oracle validity", declared: "axe runs on >=22 of 24 pages; >=1 violation on >=12 distinct pages",
    observed: `axe ran on ${pagesMeasured}; ${withViol} pages had >=1 violation`,
    verdict: pagesMeasured >= 22 && withViol >= 12 ? "PASS" : "FAIL",
  };
  // G1
  const g1 = {
    gate: "G1 repairable share (arm B)", declared: "arm B eliminates >= 30% of arm-0 AA-tagged violation instances",
    observed: `${(B.aa_share_eliminated * 100).toFixed(1)}% (${B.aa_eliminated} of ${B.before_aa})`,
    verdict: B.aa_share_eliminated >= 0.30 ? "PASS" : "FAIL",
  };
  // G2
  const g2 = {
    gate: "G2 no fabrication (arm B)", declared: "arm B fabrication rate <= 0.02",
    observed: B.fabrication_rate === null ? "no repairs applied" : B.fabrication_rate.toFixed(4),
    verdict: B.fabrication_rate !== null && B.fabrication_rate <= 0.02 ? "PASS" : "FAIL",
  };
  // G3, per frame, for both arms
  const g3 = {
    gate: "G3 no regression (each arm, every frame)", declared: "newly introduced <= 1% of eliminated, in every frame",
    observed: {},
    verdict: "PASS",
  };
  for (const [label, row] of [["A", A], ["B", B]]) {
    for (const [f, v] of Object.entries(row.frames)) {
      if (v.eliminated === 0 && v.introduced === 0) continue;
      const ratio = v.eliminated ? v.introduced / v.eliminated : Infinity;
      const okk = ratio <= 0.01;
      if (!okk) g3.verdict = "FAIL";
      g3.observed[`arm ${label} frame ${f}`] =
        `${v.introduced} new / ${v.eliminated} eliminated = ${(ratio * 100).toFixed(1)}% ${okk ? "" : "<-- FAIL"}`;
    }
  }
  // G4
  const g4 = {
    gate: "G4 population (arm B)", declared: "repairs applied on >= 8 distinct pages, >= 3 frames",
    observed: `${B.pages_with_repair} pages; ${Object.keys(B.frames).length} frames`,
    verdict: B.pages_with_repair >= 8 && Object.keys(B.frames).length >= 3 ? "PASS" : "FAIL",
  };

  const out = { run: run || "2 (canonical)", arm0: arm0.summary, A, B, gates: [g0, g1, g2, g3, g4],
    incomplete: arm0.incomplete };
  fs.writeFileSync(path.join(H.HERE, `gates${run ? "-" + run : ""}.json`), JSON.stringify(out, null, 1) + "\n");

  const line = (g) => `  ${g.verdict === "PASS" ? "PASS" : "FAIL"}  ${g.gate}\n        declared: ${g.declared}\n        observed: ${typeof g.observed === "string" ? g.observed : JSON.stringify(g.observed, null, 2).replace(/\n/g, "\n        ")}`;
  console.log(`\n=== E162 gate table [run ${out.run}] ===`);
  for (const g of [g0, g1, g2, g3, g4]) console.log(line(g));
  console.log("\n=== arm summary ===");
  console.log(JSON.stringify({ A, B }, null, 1));
}

main();