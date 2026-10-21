#!/usr/bin/env node
// E202 gate computation. Reads only recorded bytes (results-arms.json,
// results-control.json, fixtures/k1.html, pages/) and prints G1..G5, K1..K3
// and the declared baseline-dominance comparison. No thresholds are set here;
// they live in PROTOCOL.md and are copied verbatim into the verdict table.
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");

const HERE = __dirname;
const arms = JSON.parse(fs.readFileSync(path.join(HERE, "results-arms.json"), "utf8"));
const control = JSON.parse(fs.readFileSync(path.join(HERE, "results-control.json"), "utf8"));

// The predicate from run-arms.js, copied unchanged so an arm's own record is
// never the thing that decides whether it worked.
function isSelfLink(el) {
  const href = el.getAttribute("href");
  const name = el.getAttribute("name");
  const id = el.id || "";
  const empty = (el.textContent || "").trim() === "" &&
                !el.querySelector("img[alt]:not([alt=''])");
  if (!empty) return false;
  if (href !== null) {
    if (href === "") return true;
    if (href.startsWith("#")) {
      const frag = decodeURIComponent(href.slice(1));
      return frag === id || frag === name;
    }
    return false;
  }
  return name !== null && !id;
}

function key(v) {
  // An instance is (rule id, resolved target). Targets are recorded as arrays.
  return v.id + " :: " + (v.target || []).join(" >> ");
}

function aa(v) { return (v.wcag || []).length > 0; }

// --- K1 -------------------------------------------------------------------
const k1Arm0 = control.arms["0"].violations.filter(v => v.id === "link-name");
const k1Arm2 = control.arms["2"].violations.filter(v => v.id === "link-name");
const k1BareReported = k1Arm0.some(v => (v.target || []).includes("#bare-anchor")) &&
                       k1Arm2.some(v => (v.target || []).includes("#bare-anchor"));
const k1HiddenSilent = k1Arm2.every(v => !(v.target || []).some(t => /codelineno/.test(t))) &&
                       k1Arm2.length < k1Arm0.length;

const perPage = [];
let totals = { aa0: 0, aaSelf: 0, eliminated: 0, stillThere: 0,
               addedStrings: 0, newRules: [], aaIncreased: [],
               survivalWanted: 0, survivalAlive: 0, lostTargets: 0,
               arm2ClassGone: 0, arm2ClassTotal: 0 };

for (const p of arms.pages) {
  const row = { url: p.url, host: p.host };
  const a0 = p.arms["0"], a1 = p.arms["1"], a2 = p.arms["2"], a3 = p.arms["3"];
  if (!a0 || !a1 || !a2 || !a3) { row.error = "an arm is missing"; perPage.push(row); continue; }
  if (a0.error || a1.error || a2.error || a3.error) {
    row.error = JSON.stringify({ a0: a0.error, a1: a1.error, a2: a2.error, a3: a3.error });
    perPage.push(row); continue;
  }

  // Resolve arm 0's AA instances against the fetched bytes.
  const dom = new JSDOM(fs.readFileSync(path.join(HERE, p.file), "utf8"), { url: p.url });
  const doc = dom.window.document;
  const selfLinkTargets = new Set();
  const aaInstances = a0.violations.filter(aa);
  for (const v of aaInstances) {
    let el = null;
    for (const sel of (v.target || [])) {
      try { el = doc.querySelector(sel); if (el) break; } catch (e) { /* unresolvable */ }
    }
    if (el && el.tagName && /^(A|AREA)$/.test(el.tagName) && isSelfLink(el)) {
      selfLinkTargets.add(key(v));
    }
  }
  dom.window.close();

  const arm1Keys = new Set(a1.violations.map(key));
  const arm2Keys = new Set(a2.violations.map(key));
  const selfArr = [...selfLinkTargets];
  const eliminated = selfArr.filter(k => !arm1Keys.has(k));
  const still = selfArr.filter(k => arm1Keys.has(k));
  const arm2Gone = selfArr.filter(k => !arm2Keys.has(k));

  const rules0 = new Set(a0.violations.map(v => v.id));
  const rules1 = new Set(a1.violations.map(v => v.id));
  const newRules = [...rules1].filter(r => !rules0.has(r));
  const aa0 = a0.violations.filter(aa).length;
  const aa1 = a1.violations.filter(aa).length;

  const added = { "0": a0.addedStrings || [], "1": a1.addedStrings || [],
                  "2": a2.addedStrings || [], "3": a3.addedStrings || [] };

  row.aa_arm0 = aa0;
  row.aa_arm1 = aa1;
  row.aa_selflink_arm0 = selfArr.length;
  row.eliminated_arm1 = eliminated.length;
  row.still_arm1 = still.length;
  row.eliminated_arm2 = arm2Gone.length;
  row.g1_rate = selfArr.length ? eliminated.length / selfArr.length : null;
  row.new_rules_arm1 = newRules;
  row.aa_increased = aa1 > aa0;
  row.added_strings = Object.values(added).flat().length;
  row.survival = a1.survival || null;
  row.rewritten = (a1.record && a1.record.rewritten || []).length;
  row.lost_targets_arm3 = a3.lostTargets || 0;

  totals.aa0 += aa0;
  totals.aaSelf += selfArr.length;
  totals.eliminated += eliminated.length;
  totals.stillThere += still.length;
  totals.arm2ClassGone += arm2Gone.length;
  totals.arm2ClassTotal += selfArr.length;
  totals.addedStrings += row.added_strings;
  if (newRules.length) totals.newRules.push(...newRules.map(r => p.url + " " + r));
  if (row.aa_increased) totals.aaIncreased.push(p.url);
  if (a1.survival) { totals.survivalWanted += a1.survival.wanted; totals.survivalAlive += a1.survival.alive; }
  totals.lostTargets += row.lost_targets_arm3;

  perPage.push(row);
}
dom: void 0;

const verdict = {
  k1_oracle_sees_css: {
    bare_reported_without_and_with_css: k1BareReported,
    css_hidden_not_reported: k1HiddenSilent,
    arm0_link_name: k1Arm0.length,
    arm2_link_name: k1Arm2.length,
    pass: k1BareReported && k1HiddenSilent,
  },
  g1_elimination: {
    aa_selflink_instances: totals.aaSelf,
    eliminated_by_arm1: totals.eliminated,
    still_reported: totals.stillThere,
    rate: totals.aaSelf ? +(totals.eliminated / totals.aaSelf).toFixed(6) : null,
    declared: ">= 0.90", kill: "< 0.60",
  },
  g2_no_fabrication: { added_strings: totals.addedStrings, declared: "0", pass: totals.addedStrings === 0 },
  g3_no_regression: { new_rules: totals.newRules, pages_with_aa_increase: totals.aaIncreased,
    pass: totals.newRules.length === 0 && totals.aaIncreased.length === 0 },
  g5_target_survival: { wanted: totals.survivalWanted, alive: totals.survivalAlive,
    rate: totals.survivalWanted ? +(totals.survivalAlive / totals.survivalWanted).toFixed(6) : null,
    declared: "1.0" },
  baseline_dominance: {
    class_instances: totals.arm2ClassTotal,
    eliminated_by_arm1: totals.eliminated,
    eliminated_by_arm2_css: totals.arm2ClassGone,
    arm2_equals_arm1: totals.arm2ClassGone === totals.eliminated && totals.stillThere === 0,
    note: "declared in PROTOCOL.md: if K1 passes and arm 2 removes as much of the class as arm 1, arm 1 is dominated",
  },
  arm3_price: { targets_destroyed: totals.lostTargets },
  population: { qualifying_pages: arms.pages.length, hosts: [...new Set(arms.pages.map(p => p.host))].length },
  per_page: perPage,
};

const out = path.join(HERE, "gates.json");
fs.writeFileSync(out, JSON.stringify(verdict, null, 2) + "\n");
console.log(JSON.stringify(verdict, null, 2));
console.log("wrote " + out);
