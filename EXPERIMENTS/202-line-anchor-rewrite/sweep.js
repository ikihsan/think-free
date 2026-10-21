#!/usr/bin/env node
// G0 clause 1 — "axe completes on >= 90% of fetched pages".
// Arm 0 only, every HTTP-200 page in corpus-manifest.json. Durable: after each
// page the record is written, and pages already present are skipped, so an
// interrupted run resumes instead of losing measurement. Reuses run-arms.js's
// oracle through module.exports (no second implementation).
const fs = require("fs");
const path = require("path");
const { applyArm, axeRun, withAxe } = require("./run-arms.js");

const HERE = __dirname;
const OUT = path.join(HERE, "results-sweep-arm0.json");
const man = JSON.parse(fs.readFileSync(path.join(HERE, "corpus-manifest.json"), "utf8"));

const rec = fs.existsSync(OUT)
  ? JSON.parse(fs.readFileSync(OUT, "utf8"))
  : { arm: 0, engine: null, pages: [], declared: "G0 clause 1: axe completes on >=90% of fetched pages" };
const done = new Set(rec.pages.filter(p => !p.error).map(p => p.file));

const pages = man.pages.filter(p => p.status === 200);
let ran = 0;
(async () => {
  for (const p of pages) {
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
      rec.pages.push({ url: p.url, file: p.file, qualifies: !!p.qualifies, error: String(e.message || e) });
    }
    ran++;
    fs.writeFileSync(OUT, JSON.stringify(rec, null, 1) + "\n");
    if (ran % 5 === 0) console.log(`sweep +${ran} (record now ${rec.pages.length}/${pages.length})`);
  }
  const ok = rec.pages.filter(p => !p.error).length;
  console.log(`sweep done: ${ok}/${pages.length} axe runs ok, ${ran} run this invocation`);
})();
