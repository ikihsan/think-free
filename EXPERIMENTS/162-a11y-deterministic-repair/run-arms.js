#!/usr/bin/env node
// Arms A (blanket) and B (conservative), scored against the same oracle and
// the same denominator as arm 0.
//
// For every page: parse -> axe -> repair -> re-measure. The repair is applied
// to the live DOM, so no string-rewriting hazard exists between what the
// repairer believes and what the oracle sees.
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");
const H = require("./lib/harness");
const R = require("./lib/repair");

const AA = new Set(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]);
const isAA = (tags) => tags.some((t) => AA.has(t));

// A violation instance, identified by rule + target path, so elimination and
// introduction are measured on the same unit in both arms.
function key(v) {
  return `${v.id}|${JSON.stringify(v.target)}`;
}

async function runPolicy(page, policy, base) {
  const raw = H.htmlFor(page);
  const serialized = H.roundTrip(raw, page.final_url);
  const dom = H.withAxe(serialized, page.final_url);
  const doc = dom.window.document;

  // Re-read the findings from the live document rather than reusing arm 0's
  // recorded ones: the node list and the targets must belong to this DOM.
  const res = await H.axeRun(dom);
  const outcome = R.repair(doc, res.violations, policy);

  const after = await H.axeRun(dom);
  dom.window.close();

  const beforeByKey = new Map(res.violations.map((v) => [key(v), v]));
  const afterKeys = new Set(after.violations.map(key));

  let eliminated = 0, introduced = 0;
  const eliminatedByRule = {}, introducedByRule = {};
  for (const k of beforeByKey.keys()) if (!afterKeys.has(k)) {
    eliminated += 1;
    const r = beforeByKey.get(k).id;
    eliminatedByRule[r] = (eliminatedByRule[r] || 0) + 1;
  }
  for (const k of afterKeys) if (!beforeByKey.has(k)) {
    introduced += 1;
    const r = after.violations.find((v) => key(v) === k).id;
    introducedByRule[r] = (introducedByRule[r] || 0) + 1;
  }

  const baseAA = base.filter((v) => isAA(v.tags)).length;
  const beforeAA = res.violations.filter((v) => isAA(v.tags)).length;
  const afterAA = after.violations.filter((v) => isAA(v.tags)).length;

  return {
    id: page.id, frame: page.frame, url: page.final_url,
    before_total: res.violations.length,
    after_total: after.violations.length,
    before_aa: beforeAA, after_aa: afterAA,
    arm0_aa: baseAA,
    eliminated, introduced,
    eliminated_by_rule: eliminatedByRule,
    introduced_by_rule: introducedByRule,
    repairs_applied: outcome.applied_count,
    repairs_fabricated: outcome.fabricated_count,
    fabrication_rate: outcome.fabrication_rate,
    repairs_by_rule: outcome.by_rule,
    repair_log: outcome.log.slice(0, 400),
    fabricated_examples: outcome.fabricated.slice(0, 60),
  };
}

async function main() {
  const arm0 = JSON.parse(fs.readFileSync(path.join(H.HERE, "results-arm0.json"), "utf8"));
  const byId = {};
  for (const p of arm0.pages) {
    const all = [];
    // arm0 stores slim rows without targets; pull the AA flag from stored tags.
    for (const v of p.violations || []) all.push({ id: v.id, tags: v.tags, target: [] });
    byId[p.id] = all;
  }
  const pages = H.loadCorpus().filter((p) => byId[p.id]);
  const out = { arms: {}, pages_missing_from_arm0: [] };

  for (const policy of ["blanket", "conservative"]) {
    const label = policy === "blanket" ? "A" : "B";
    const rows = [];
    const outfile = path.join(H.HERE, `results-arm${label}.json`);
    const done = new Set();
    if (fs.existsSync(outfile)) {
      const prev = JSON.parse(fs.readFileSync(outfile, "utf8"));
      for (const r of prev.pages || []) { rows.push(r); done.add(r.id); }
      process.stdout.write(`arm ${label}: resuming with ${rows.length} pages\n`);
    }
    for (const p of pages) {
      if (done.has(p.id)) continue;
      let row;
      try {
        row = await runPolicy(p, policy, byId[p.id]);
      } catch (err) {
        row = { id: p.id, frame: p.frame, url: p.final_url, error: String(err).slice(0, 200) };
      }
      rows.push(row);
      fs.writeFileSync(outfile, JSON.stringify({ arm: label, policy, pages: rows }, null, 1) + "\n");
      if (!row.error) {
        process.stdout.write(`arm ${label} ${row.id} elim ${String(row.eliminated).padStart(4)}  new ${String(row.introduced).padStart(4)}  applied ${String(row.repairs_applied).padStart(4)}  fab ${row.repairs_fabricated}\n`);
      } else {
        process.stdout.write(`arm ${label} ${row.id} ERROR ${row.error}\n`);
      }
    }
    out.arms[label] = summarise(label, policy, rows);
  }

  fs.writeFileSync(path.join(H.HERE, "results-arms.json"), JSON.stringify(out, null, 1) + "\n");
  console.log("\n" + JSON.stringify(out, null, 1));
}

function summarise(label, policy, rows) {
  const ok = rows.filter((r) => !r.error);
  const s = (k) => ok.reduce((a, r) => a + (r[k] || 0), 0);
  const arm0AA = s("arm0_aa"), beforeAA = s("before_aa"), afterAA = s("after_aa");
  const base0 = ok.reduce((a, r) => a + r.before_total, 0);
  const after0 = ok.reduce((a, r) => a + r.after_total, 0);
  const elimAA = Math.max(0, beforeAA - afterAA);
  const applied = s("repairs_applied"), fab = s("repairs_fabricated");
  const frames = {};
  for (const r of ok) {
    frames[r.frame] = frames[r.frame] || { eliminated: 0, introduced: 0 };
    frames[r.frame].eliminated += r.eliminated;
    frames[r.frame].introduced += r.introduced;
  }
  return {
    arm: label, policy, pages: ok.length,
    before_total: base0, after_total: after0,
    before_aa: beforeAA, after_aa: afterAA, arm0_aa: arm0AA,
    eliminated: s("eliminated"), introduced: s("introduced"),
    eliminated_share_of_aa: beforeAA ? elimAA / beforeAA : null,
    aa_removed_by_count: elimAA,
    repairs_applied: applied, repairs_fabricated: fab,
    fabrication_rate: applied ? fab / applied : null,
    pages_with_repair: ok.filter((r) => r.repairs_applied > 0).length,
    frames_affected: Object.keys(frames).filter((f) => frames[f].eliminated > 0).length,
    frames,
  };
}

main().catch((e) => { console.error(e); process.exit(1); });