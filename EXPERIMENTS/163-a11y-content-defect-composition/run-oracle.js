#!/usr/bin/env node
// E163 arm 0 - the oracle over the union of both arms' pages.
//
// Arm 1 (the 27 pages E162 hashed) is REUSED from E162's results-arm0.json, so
// the 33 content-bearing defects E162 reported stay exactly the 33 they were.
// Arm 2 (the 45 functional sub-pages) is measured here with the same oracle and
// the same harness settings: axe-core 4.14.0 in jsdom, default ruleset, page
// scripts not executed (E162 Amendment 2).
//
// Resumable: the output file is rewritten after every page and ids already
// present are skipped.
const fs = require("fs");
const path = require("path");
const E162 = "../162-a11y-deterministic-repair";
const H = require(path.join(__dirname, E162, "lib", "harness"));

const OUT = path.join(__dirname, "results-arm0.json");

function newPage(rec) {
  return {
    id: rec.id, frame: rec.frame, url: rec.final_url, sha256: rec.sha256,
    bytes: rec.bytes, file: path.relative(__dirname, path.join(__dirname, rec.file)),
  };
}

async function main() {
  let out = { arm: "0-union", pages: [], incomplete: {} };
  if (fs.existsSync(OUT)) {
    const prev = JSON.parse(fs.readFileSync(OUT, "utf8"));
    if (prev.pages && prev.pages.length) {
      out = prev;
      process.stdout.write(`resuming: ${out.pages.length} pages already measured\n`);
    }
  }

  // Arm 1, reused verbatim.
  const e162 = JSON.parse(fs.readFileSync(path.join(__dirname, E162, "results-arm0.json"), "utf8"));
  for (const p of e162.pages) {
    if (out.pages.some((x) => x.id === `162:${p.id}`)) continue;
    out.pages.push(Object.assign({}, p, { id: `162:${p.id}`, arm: "1" }));
  }
  // Arm 2, measured now.
  const man = JSON.parse(fs.readFileSync(path.join(__dirname, "corpus-manifest.json"), "utf8"));
  for (const rec of man.pages) {
    if (out.pages.some((x) => x.id === rec.id)) continue;
    const raw = fs.readFileSync(path.join(__dirname, rec.file));
    let res, page;
    try {
      const dom = H.withAxe(H.roundTrip(raw.toString("utf8"), rec.final_url), rec.final_url);
      res = await H.axeRun(dom);
      dom.window.close();
    } catch (err) {
      page = { id: rec.id, frame: rec.frame, url: rec.final_url, arm: "2", error: String(err).slice(0, 200) };
      out.pages.push(page);
      fs.writeFileSync(OUT, JSON.stringify(out, null, 1) + "\n");
      console.log(`${rec.id} ERROR ${page.error}`);
      continue;
    }
    for (const [k, v] of Object.entries(res.incomplete)) out.incomplete[k] = (out.incomplete[k] || 0) + v;
    page = {
      id: rec.id, frame: rec.frame, url: rec.final_url, sha256: rec.sha256, bytes: rec.bytes,
      arm: "2", instances: res.violations.length, engine: res.testEngine,
      violations: res.violations.map((v) => ({ id: v.id, impact: v.impact, tags: v.tags, html: v.html })),
    };
    out.pages.push(page);
    fs.writeFileSync(OUT, JSON.stringify(out, null, 1) + "\n");
    console.log(`${rec.id} ${String(res.violations.length).padStart(5)} violations (${rec.frame})`);
  }
  fs.writeFileSync(OUT, JSON.stringify(out, null, 1) + "\n");

  const measured = out.pages.filter((p) => !p.error);
  const inst = measured.reduce((a, p) => a + (p.instances || 0), 0);
  console.log(`\nunion: ${measured.length} pages measured of ${man.pages.length + e162.pages.length}`,
    `| ${measured.filter((p) => (p.instances || 0) > 0).length} with >=1 violation | ${inst} instances`);
}

main().catch((e) => { console.error(e); process.exit(1); });