#!/usr/bin/env node
// Per-page timing probe: which pages are slow, and where does the time go.
const H = require("./lib/harness");

(async () => {
  const only = process.argv[2];
  for (const p of H.loadCorpus()) {
    if (only && p.id !== only) continue;
    let t = Date.now();
    const raw = H.htmlFor(p);
    const serialized = H.roundTrip(raw, p.final_url);
    const tRt = Date.now() - t;
    t = Date.now();
    let n = -1;
    try {
      const dom = H.withAxe(serialized, p.final_url);
      const r = await H.axeRun(dom);
      n = r.violations.length;
      dom.window.close();
    } catch (e) { n = -2; }
    const tAx = Date.now() - t;
    console.log(`${p.id} ${String(p.bytes).padStart(8)}B  roundtrip ${String(tRt).padStart(6)}ms  axe ${String(tAx).padStart(7)}ms  violations ${n}`);
  }
})();