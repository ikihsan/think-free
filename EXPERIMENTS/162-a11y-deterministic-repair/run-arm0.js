#!/usr/bin/env node
// Arm 0 - the status quo. Measure what real pages carry, and at what volume,
// before any repairer exists. This fixes the denominator for every arm.
const fs = require("fs");
const path = require("path");
const H = require("./lib/harness");

const OUTFILE = path.join(H.HERE, "results-arm0.json");

function flush(out, ruleSets) {
  const rules = {};
  for (const [k, v] of Object.entries(ruleSets)) {
    rules[k] = { instances: v.instances, pages: v.pages.size, impact: v.impact,
      tags: v.tags, help: v.help, sampleHtml: v.sampleHtml };
  }
  out.byRule = rules;
  out.summary = {
    pages_in_manifest: out.pages.length,
    pages_axe_ran_on: out.pages.filter((p) => !p.error).length,
    pages_with_at_least_one_violation: out.pages.filter((p) => (p.instances || 0) > 0).length,
    total_instances: out.pages.reduce((a, p) => a + (p.instances || 0), 0),
  };
  fs.writeFileSync(OUTFILE, JSON.stringify(out, null, 1) + "\n");
}

function tally(ruleSets, v, pageId) {
  const r = ruleSets[v.id] || (ruleSets[v.id] = { instances: 0, pages: new Set(),
    impact: v.impact, tags: v.tags, help: v.help, sampleHtml: v.html });
  r.instances += 1;
  r.pages.add(pageId);
  return r;
}

async function main() {
  const pages = H.loadCorpus();
  let out = { arm: "0", pages: [], byRule: {}, incomplete: {} };
  if (fs.existsSync(OUTFILE)) {
    const prev = JSON.parse(fs.readFileSync(OUTFILE, "utf8"));
    if (prev.pages && prev.pages.length) {
      out = prev;
      out.byRule = {};
      for (const p of out.pages) {
        for (const v of p.violations || []) tally({}, v, p.id);
      }
      process.stdout.write(`resuming: ${out.pages.length} pages already measured\n`);
    }
  }
  const ruleSets = {};
  for (const p of out.pages) for (const v of p.violations || []) tally(ruleSets, v, p.id);

  for (const p of pages) {
    if (out.pages.some((x) => x.id === p.id)) continue;
    const raw = H.htmlFor(p);
    const serialized = H.roundTrip(raw, p.final_url);
    let res;
    try {
      const dom = H.withAxe(serialized, p.final_url);
      res = await H.axeRun(dom);
      dom.window.close();
    } catch (err) {
      out.pages.push({ id: p.id, frame: p.frame, url: p.final_url, error: String(err).slice(0, 200) });
      flush(out, ruleSets);
      continue;
    }
    const n = res.violations.length;
    for (const v of res.violations) tally(ruleSets, v, p.id);
    for (const [k, v] of Object.entries(res.incomplete)) {
      out.incomplete[k] = (out.incomplete[k] || 0) + v;
    }
    out.pages.push({
      id: p.id, frame: p.frame, url: p.final_url, sha256: p.sha256,
      bytes: p.bytes, instances: n, engine: res.testEngine,
      violations: res.violations.map((v) => ({ id: v.id, impact: v.impact, tags: v.tags, html: v.html })),
    });
    process.stdout.write(`${p.id} ${String(n).padStart(5)} violations  (${p.frame})\n`);
    flush(out, ruleSets);
  }
  flush(out, ruleSets);

  console.log("\n=== arm 0 summary ===");
  console.log(JSON.stringify(out.summary, null, 1));
  console.log("\n=== violations by rule ===");
  const rules = {};
  for (const [k, v] of Object.entries(out.byRule)) {
    rules[k] = { instances: v.instances, pages: v.pages.size, impact: v.impact,
      tags: v.tags, help: v.help, sampleHtml: v.sampleHtml };
  }
  const sorted = Object.entries(rules).sort((a, b) => b[1].instances - a[1].instances);
  let tot = 0;
  for (const [k, v] of sorted) {
    tot += v.instances;
    const aa = v.tags.includes("wcag2a") || v.tags.includes("wcag2aa") ||
               v.tags.includes("wcag21a") || v.tags.includes("wcag21aa") || v.tags.includes("wcag22aa");
    console.log(`${String(v.instances).padStart(6)}  ${String(v.pages).padStart(3)}pg  ${aa ? "AA " : "   "} ${k}  [${v.impact}]`);
  }
  console.log(`${String(tot).padStart(6)}  TOTAL`);
  console.log("\n=== incomplete (oracle could not decide, no layout in jsdom) ===");
  console.log(JSON.stringify(out.incomplete));
}

main().catch((e) => { console.error(e); process.exit(1); });