#!/usr/bin/env node
// E163 driver - the repaired oracle loop.
//
// Same resume logic and output schema as run-oracle.js (which see), but each
// page is measured by a `page-runner.js` subprocess under a hard external
// timeout, so a page whose axe.run blocks the event loop is recorded as an
// error and skipped instead of hanging the loop forever. See page-runner.js
// for why. External timeout: 300s per page (2.5x the harness's own declared
// 240s budget). Arm 1 pages are reused from E162 exactly as before.
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const HERE = __dirname;
const OUT = path.join(HERE, "results-arm0.json");
const E162 = path.join(HERE, "..", "162-a11y-deterministic-repair");
const EXTERNAL_TIMEOUT_MS = 300000;

function readOut() {
  if (fs.existsSync(OUT)) {
    const prev = JSON.parse(fs.readFileSync(OUT, "utf8"));
    if (prev.pages && prev.pages.length) return prev;
  }
  return { arm: "0-union", pages: [], incomplete: {} };
}

function main() {
  const out = readOut();
  const man = JSON.parse(fs.readFileSync(path.join(HERE, "corpus-manifest.json"), "utf8"));

  const done = new Set(out.pages.map((p) => p.id));
  const todo = man.pages.filter((p) => !done.has(p.id));
  console.log(`${out.pages.length} pages already measured; ${todo.length} remaining`);

  for (const rec of todo) {
    const f = path.join(HERE, "raw", `page-${rec.id}.json`);
    let recOut = null, how = null;
    const r = spawnSync("node", [path.join(HERE, "page-runner.js"), rec.id], {
      timeout: EXTERNAL_TIMEOUT_MS, encoding: "utf8",
    });
    if (fs.existsSync(f)) {
      try { recOut = JSON.parse(fs.readFileSync(f, "utf8")); } catch (e) { recOut = null; }
    }
    if (recOut && !recOut.error) {
      out.pages.push(recOut);
    } else {
      // The runner writes its own error record on any failure (including the
      // harness's own "axe timeout"). No record means the subprocess was killed
      // externally while its event loop was blocked - that is the case the
      // in-process timer cannot catch.
      const err = (recOut && recOut.error)
        || (r.error && r.error.message)
        || (r.signal ? `killed by ${r.signal} after ${EXTERNAL_TIMEOUT_MS / 1000}s (event loop blocked)` : null)
        || `runner failed (status ${r.status})`;
      out.pages.push(recOut || {
        id: rec.id, frame: rec.frame, url: rec.final_url, arm: "2", error: String(err).slice(0, 200),
      });
    }
    fs.writeFileSync(OUT, JSON.stringify(out, null, 1) + "\n");
    const last = out.pages[out.pages.length - 1];
    console.log(`${last.id} ${last.error ? "ERROR " + last.error : last.instances + " violations"} (${rec.frame})`);
  }

  const measured = out.pages.filter((p) => !p.error);
  const inst = measured.reduce((a, p) => a + (p.instances || 0), 0);
  console.log(`\nunion: ${measured.length} pages measured of ${man.pages.length + 27}`,
    `| ${measured.filter((p) => (p.instances || 0) > 0).length} with >=1 violation | ${inst} instances`);
}

main();
