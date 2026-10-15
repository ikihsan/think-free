#!/usr/bin/env node
// One repair codebase, two policies. The arms differ by one field per rule -
// `derivable` - so the contrast is an ablation of the fabrication policy and
// not a comparison of two programs written by different people.
//
// A repair is FABRICATED when it puts a user-facing string into the document
// that no author wrote: a value absent from the page's own text and attributes
// before any repair ran. Every such string is a literal in the rule table, which
// is what makes the measure mechanical rather than judged.
//
// This file is the driver - the loop that applies one arm to one document. The
// rules live in `./rules`, the three DOM readers in `./dom`, and the
// defect-id-to-rule lookup in `./dispatch`.

const { ruleFor, permitted } = require("./dispatch");
const { sel } = require("./dom");
const { RULES } = require("./rules");

/**
 * Apply one arm's repairs to a document.
 * policy: "blanket" (arm A) | "conservative" (arm B)
 *
 * `violations` is the flat per-node list this experiment's harness produces:
 * one entry per axe node, each carrying `id` and `target`. It is regrouped by
 * rule here, because that grouping is an implementation detail of axe rather
 * than something a caller should have to reconstruct.
 *
 * Each (rule, target) pair is visited at most once, so no repair is counted
 * twice and no rule sees a document a later rule already changed.
 *
 * `table` defaults to the canonical rule table; `makeRepair` binds another one,
 * which is how run 1 stays replayable from `./rules-run1`.
 */
function repair(doc, violations, policy, table) {
  const lookup = table || { RULES, ruleFor, permitted };
  const grouped = new Map();
  for (const v of violations || []) {
    if (!grouped.has(v.id)) grouped.set(v.id, []);
    grouped.get(v.id).push(v.target);
  }

  const log = [];
  const seen = new Set();
  const counts = {};
  let skipped = 0;

  for (const [id, targets] of grouped) {
    const rule = lookup.ruleFor(id);
    if (!rule) {
      counts[id] = counts[id] || { applied: 0, abstained: 0, not_in_table: 0 };
      counts[id].not_in_table += targets.length;
      skipped += targets.length;
      continue;
    }
    if (!lookup.permitted(policy, rule)) {
      counts[rule.id] = counts[rule.id] || { applied: 0, abstained: 0, not_in_table: 0 };
      counts[rule.id].abstained += targets.length;
      skipped += targets.length;
      log.push({ rule: rule.id, action: "not-permitted-in-this-arm", nodes: targets.length, fabricated: false });
      continue;
    }
    for (const target of targets) {
      const key = `${rule.id}|${JSON.stringify(target)}`;
      if (seen.has(key)) continue;
      seen.add(key);
      const el = sel(doc, target);
      counts[rule.id] = counts[rule.id] || { applied: 0, abstained: 0, not_in_table: 0 };
      if (!el) { counts[rule.id].abstained += 1; continue; }
      let ok = false;
      const before = log.length;
      try { ok = rule.apply(el, doc, log, policy); } catch (e) { ok = false; }
      if (ok) counts[rule.id].applied += 1;
      else {
        counts[rule.id].abstained += 1;
        if (log.length === before) {
          log.push({ rule: rule.id, action: "abstain", reason: "no derivable value", fabricated: false });
        }
      }
    }
  }

  // An "applied" repair is one that changed the document. Abstentions and
  // rules this arm may not touch at all are recorded, but never counted as
  // repairs - otherwise a policy that does nothing would score perfectly.
  const NO_CHANGE = new Set(["abstain", "not-permitted-in-this-arm"]);
  const applied = log.filter((r) => !NO_CHANGE.has(r.action));
  const fabricated = applied.filter((r) => r.fabricated);
  const declined = log.filter((r) => NO_CHANGE.has(r.action));
  return {
    log, applied, fabricated, declined, by_rule: counts, skipped,
    applied_count: applied.length,
    fabricated_count: fabricated.length,
    fabrication_rate: applied.length ? fabricated.length / applied.length : null,
  };
}

/** The same driver, bound to another rule table. Used to keep run 1 replayable. */
function makeRepair(table) {
  return (doc, violations, policy) => repair(doc, violations, policy, table);
}

module.exports = { repair, makeRepair, RULES, ruleFor, permitted };