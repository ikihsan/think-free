#!/usr/bin/env node
// E202 G0 sweep, resumed in disjoint shards (see AMENDMENT-2.md).
//
// Why: sweep.js is single-process and the three axe-timeout pages cost 12
// minutes by themselves; the session needed the G0 record complete while other
// work ran. Nothing about the per-page measurement changes: this file reuses
// sweep.js's exact oracle through the same module.exports (applyArm, withAxe,
// axeRun), the same 240 s timeout, the same page set, and the same record
// shape. Only the partition and the output file differ.
//
// Usage: SWARD=<i> SWN=<n> node shard-sweep.js
//   todo = every HTTP-200 page in corpus-manifest.json that has no *successful*
//   record yet in results-sweep-arm0.json (axe-timeout pages are retried once,
//   exactly as sweep.js's own resume rule intends: done excludes errors).
//   todo[k] goes to shard (k mod n); shards therefore never share a page.
// Output: results-sweep-arm0-part<i>.json, written durably after every page.
const fs = require("fs");
const path = require("path");
const { applyArm, axeRun, withAxe } = require("./run-arms.js");

const HERE = __dirname;
const MAIN = path.join(HERE, "results-sweep-arm0.json");
const I = parseInt(process.env.SWARD || "0", 10);
const N = parseInt(process.env.SWN || "1", 10);
if (!Number.isInteger(I) || !Number.isInteger(N) || I < 0 || I >= N) {
  console.error(`bad shard ${process.env.SWARD}/${process.env.SWN}`);
  process.exit(1);
}
const OUT = path.join(HERE, `results-sweep-arm0-part${I}.json`);

const man = JSON.parse(fs.readFileSync(path.join(HERE, "corpus-manifest.json"), "utf8"));
const main = JSON.parse(fs.readFileSync(MAIN, "utf8"));
const ok = new Set(main.pages.filter(p => !p.error).map(p => p.file));

const todo = man.pages.filter(p => p.status === 200 && !ok.has(p.file));
const mine = todo.filter((p, k) => k % N === I);

const rec = fs.existsSync(OUT)
  ? JSON.parse(fs.readFileSync(OUT, "utf8"))
  : { arm: 0, engine: null, shard: I, of: N, pages: [],
      declared: "G0 clause 1 (sharded resume, AMENDMENT-2): axe completes on >=90% of fetched pages" };
const done = new Set(rec.pages.map(p => p.file));

(async () => {
  console.log(`shard ${I}/${N}: todo=${todo.length} mine=${mine.length} already=${done.size}`);
  let ran = 0;
  for (const p of mine) {
    if (done.has(p.file)) continue;
    const html = fs.readFileSync(path.join(HERE, p.file), "utf8");
    const r = applyArm(html, 0);
    try {
      const dom = withAxe(r.html, p.url);
      const res = await axeRun(dom);
      dom.window.close();
      rec.pages.push({ url: p.url, file: p.file, qualifies: !!p.qualifies,
        n: res.violations.length, wcag: res.violations.filter(v => v.wcag.length).length,
        rules: [...new Set(res.violations.map(v => v.id))], engine: res.testEngine,
        violations: res.violations });
      rec.engine = res.testEngine;
    } catch (e) {
      rec.pages.push({ url: p.url, file: p.file, qualifies: !!p.qualifies,
        error: String(e.message || e) });
    }
    ran++;
    fs.writeFileSync(OUT, JSON.stringify(rec) + "\n");
    console.log(`shard ${I}: +${ran}/${mine.length} (record ${rec.pages.length})`);
  }
  const good = rec.pages.filter(p => !p.error).length;
  console.log(`shard ${I} done: ${good}/${mine.length} ok, ${ran} run this invocation`);
})();
