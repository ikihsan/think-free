#!/usr/bin/env node
// E202 G0 — merge the sharded sweep per AMENDMENT-2 and compute G0 clause 1
// under the three denominators AMENDMENT-2 required and the two merge readings
// AMENDMENT-3 declared. Reads only recorded bytes: results-sweep-arm0.json,
// results-sweep-arm0-part{0,1,2}.json, corpus-manifest.json. Sets no threshold;
// they live in PROTOCOL.md and are copied into the verdict object.
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const read = (f) => JSON.parse(fs.readFileSync(path.join(HERE, f), "utf8"));

const man = read("corpus-manifest.json");
const main = read("results-sweep-arm0.json");
const parts = [0, 1, 2].map((i) => read(`results-sweep-arm0-part${i}.json`));

// --- sweep records indexed by file ----------------------------------------
// file -> [{src, ok, n, wcag, rules, error}]
const sweeps = new Map();
function add(src, rec) {
  for (const p of rec.pages) {
    if (!sweeps.has(p.file)) sweeps.set(p.file, []);
    sweeps.get(p.file).push({
      src, ok: !p.error, error: p.error || null,
      n: p.n, wcag: p.wcag, rules: p.rules || [],
    });
  }
}
add("main", main);
parts.forEach((p, i) => add(`part${i}`, p));

// --- duplicate census (AMENDMENT-3 §1/§2) --------------------------------
const dupFiles = [...sweeps.entries()].filter(([, v]) => v.length > 1);
const completedDisagreements = [];
const retryPairs = [];
for (const [file, recs] of dupFiles) {
  const done = recs.filter((r) => r.ok);
  if (done.length > 1) {
    const sig = (r) => JSON.stringify([r.n, r.wcag, [...r.rules].sort()]);
    const sigs = new Set(done.map(sig));
    if (sigs.size > 1) completedDisagreements.push({ file, records: done });
  }
  if (done.length && recs.some((r) => !r.ok)) retryPairs.push({ file, records: recs.map(r => r.src + ":" + (r.ok ? "ok" : r.error)) });
}

// --- manifest census ------------------------------------------------------
const recFiles = man.pages.map((p) => p.file);
const firstIndex = new Map();
recFiles.forEach((f, i) => { if (!firstIndex.has(f)) firstIndex.set(f, i); });

const DEN = {
  D200: man.pages.filter((p) => p.status === 200),
  DALL: man.pages,
  DBODY: man.pages.filter((p) => (p.bytes || 0) > 0),
};

// file outcome under each reading
function completed(file, reading) {
  const recs = sweeps.get(file) || [];
  if (recs.length === 0) return false;               // never handed to the oracle
  const anyOk = recs.some((r) => r.ok);
  if (reading === "primary") return anyOk;
  // literal: a file whose records disagree (timeout vs completion) stops the
  // merge (AMENDMENT-3 §1), so it counts as a failure in every denominator.
  const outs = new Set(recs.map((r) => (r.ok ? "ok" : "err")));
  if (outs.size > 1) return false;
  return anyOk;
}

function rate(num, den) { return den ? +(num / den).toFixed(6) : null; }

function underReading(reading) {
  const out = {};
  for (const [label, records] of Object.entries(DEN)) {
    const files = [...new Set(records.map((p) => p.file))];
    const recOk = records.filter((p) => completed(p.file, reading)).length;
    const fileOk = files.filter((f) => completed(f, reading)).length;
    out[label] = {
      records: { num: recOk, den: records.length, rate: rate(recOk, records.length) },
      files: { num: fileOk, den: files.length, rate: rate(fileOk, files.length) },
      never_handed: files.filter((f) => !(sweeps.get(f) || []).length).length,
    };
  }
  return out;
}

// --- merged record set (AMENDMENT-2 order) --------------------------------
const mergedOrder = [];
const seen = new Set();
for (const p of main.pages) {                       // main's successful pages first
  if (!p.error && !seen.has(p.file)) { seen.add(p.file); mergedOrder.push(p.file); }
}
for (const part of parts) {                         // then every part file
  for (const p of part.pages) { if (!seen.has(p.file)) { seen.add(p.file); mergedOrder.push(p.file); } }
}
mergedOrder.sort((a, b) => (firstIndex.get(a) ?? 1e9) - (firstIndex.get(b) ?? 1e9));

const blocked = [...sweeps.entries()]
  .filter(([, v]) => new Set(v.map((r) => (r.ok ? "ok" : "err"))).size > 1)
  .map(([f]) => f);

// --- G0 clause 2 and G4 ---------------------------------------------------
const qualifying = man.pages.filter((p) => p.qualifies);
const qFiles = [...new Set(qualifying.map((p) => p.file))];
const qWithAA = qFiles.filter((f) => {
  const recs = (sweeps.get(f) || []).filter((r) => r.ok);
  return recs.some((r) => (r.wcag || 0) > 0);
});
const qHosts = [...new Set(qualifying.map((p) => p.host))];

const engines = new Set();
for (const rec of [main, ...parts]) for (const p of rec.pages) if (p.engine) engines.add(p.engine.version || JSON.stringify(p.engine));

const primary = underReading("primary");
const literal = underReading("literal");
const p200 = primary.D200;
const l200 = literal.D200;

const verdict = {
  g0_clause1: {
    declared: "axe completes on >= 0.90 of fetched pages",
    declared_denominator: "D200 (HTTP 200), AMENDMENT-2",
    readings: { with_retry_supersession: primary, literal_no_supersession: literal },
    verdict_line: {
      reading_used: "with_retry_supersession (AMENDMENT-3 §1)",
      D200_records: p200.records, D200_files: p200.files,
      pass: (p200.files.rate >= 0.9),
      literal_D200_files: l200.files,
    },
    timeout_files: [...sweeps.entries()]
      .filter(([, v]) => v.every((r) => !r.ok))
      .map(([f, v]) => ({ file: f, attempts: v.length, error: v[0].error, attempts_by: v.map((r) => r.src) })),
  },
  g0_clause2: {
    declared: ">= 8 qualifying pages hold >= 1 AA-tagged instance",
    qualifying_pages: qFiles.length,
    qualifying_with_aa: qWithAA.length,
    pass: qWithAA.length >= 8,
    note: "denominator is capped by the corpus: only " + qFiles.length + " qualifying pages exist (G4)",
  },
  g4_population: {
    declared: ">= 12 qualifying pages across >= 6 hosts",
    qualifying_pages: qFiles.length, hosts: qHosts.length,
    pass: qFiles.length >= 12 && qHosts.length >= 6,
    stage1: man.stage1, stage2: man.stage2,
  },
  merge: {
    records_total: [main, ...parts].reduce((s, r) => s + r.pages.length, 0),
    distinct_files_with_sweep: sweeps.size,
    merged_records: mergedOrder.length,
    duplicate_files: dupFiles.length,
    completed_run_disagreements: completedDisagreements.length,
    completed_disagreement_detail: completedDisagreements,
    retry_pairs: retryPairs,
    files_blocking_literal_merge: blocked,
    manifest_records: man.pages.length,
    manifest_distinct_files: firstIndex.size,
  },
  engine: [...engines],
};

fs.writeFileSync(path.join(HERE, "results-g0.json"), JSON.stringify(verdict, null, 2) + "\n");
console.log(JSON.stringify(verdict, null, 2));
console.log("wrote results-g0.json");
