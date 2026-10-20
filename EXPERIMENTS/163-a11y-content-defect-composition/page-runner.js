#!/usr/bin/env node
// E163 per-page runner - the repaired instrument.
//
// Why this exists: the in-process harness timeout (PER_PAGE_TIMEOUT_MS = 240s,
// Promise.race in axeRun) cannot fire while axe-core blocks the event loop.
// On page 025 (seattle.gov, 462KB) axe.run burned CPU for >15 minutes without
// completing and without rejecting; the 240s timer never ran. The oracle was
// killed and the remaining pages are measured here, one subprocess per page,
// under a hard external timeout. Population, oracle (axe-core 4.14.0 in jsdom,
// scripts not executed), classification rule and gates are all unchanged; the
// instrument now honours its own declared 240s budget externally.
//
// Usage: node page-runner.js <manifest-id>
// Writes raw/page-<id>.json atomically: the page record in run-oracle.js's
// schema, or {id, frame, url, arm:"2", error}. Always writes something.
const fs = require("fs");
const path = require("path");
const H = require(path.join(__dirname, "..", "162-a11y-deterministic-repair", "lib", "harness"));

const HERE = __dirname;

function write(rec) {
  const f = path.join(HERE, "raw", `page-${rec.id}.json`);
  const tmp = f + ".tmp";
  fs.writeFileSync(tmp, JSON.stringify(rec));
  fs.renameSync(tmp, f);
}

async function main() {
  const id = process.argv[2];
  const man = JSON.parse(fs.readFileSync(path.join(HERE, "corpus-manifest.json"), "utf8"));
  const rec = man.pages.find((p) => p.id === id);
  if (!rec) throw new Error(`id not in manifest: ${id}`);
  const raw = fs.readFileSync(path.join(HERE, rec.file));
  const dom = H.withAxe(H.roundTrip(raw.toString("utf8"), rec.final_url), rec.final_url);
  const res = await H.axeRun(dom);
  dom.window.close();
  write({
    id: rec.id, frame: rec.frame, url: rec.final_url, sha256: rec.sha256, bytes: rec.bytes,
    arm: "2", instances: res.violations.length, engine: res.testEngine,
    violations: res.violations.map((v) => ({ id: v.id, impact: v.impact, tags: v.tags, html: v.html })),
  });
  console.log(`${id} ${res.violations.length} violations`);
}

main().catch((e) => {
  // Re-read the manifest for the error record's fields.
  const id = process.argv[2];
  let rec = { id };
  try {
    const man = JSON.parse(fs.readFileSync(path.join(HERE, "corpus-manifest.json"), "utf8"));
    rec = man.pages.find((p) => p.id === id) || rec;
  } catch (e2) { /* keep minimal record */ }
  write({
    id: rec.id, frame: rec.frame, url: rec.final_url, arm: "2",
    error: String(e && e.message ? e.message : e).slice(0, 200),
  });
  console.error(`${id} ERROR ${e && e.message ? e.message : e}`);
  process.exit(1);
});
