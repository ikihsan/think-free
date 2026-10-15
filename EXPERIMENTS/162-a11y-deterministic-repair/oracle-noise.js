#!/usr/bin/env node
// A second measurement on the same arm-0 record, with no repair table in it at
// all: how much of what axe reports on these pages is aimed at elements that
// were never meant to be read.
//
// 90 of the 96 `link-name` violations came from one page and are Pygments
// code-line anchors: `<a id="__codelineno-0-1" href="#__codelineno-0-1"></a>`.
// They are keyboard-reachable, empty, and machine-generated. A user never
// navigates to them, but they are counted, which means the denominator every
// "how accessible is this page" number is computed from contains them.
//
// This script counts that directly, from the recorded markup only. It is a
// measurement of the ORACLE on a real population, not of any repair: what share
// of reported instances sit on elements that a page's author never wrote text
// for and never intended a user to read.
const fs = require("fs");
const path = require("path");
const H = require("./lib/harness");

// How an instance is classified. Deliberately narrow: a first version matched
// a broad id/name pattern and swept in controls that carry a proper
// `aria-label` (a Material-for-MkDocs sidebar toggle was called "generated"),
// which would have overstated this measurement. Only two buckets are claimed:
//
//   empty anchor          - `<a ...></a>` with nothing in it: focusable, and
//                           it reads nothing.
//   generated line anchor - a syntax highlighter's per-line anchor, which is
//                           plumbing, not navigation.
//
// Everything else is `content`, including labelled controls.
function classify(html) {
  const trimmed = html.trim();
  const id = (/<[^>]+\sid="([^"]*)"/.exec(trimmed) || [])[1] || "";
  const name = (/<[^>]+\sname="([^"]*)"/.exec(trimmed) || [])[1] || "";
  if (/^(__codelineno|__line|line-\d|hljs)/i.test(id) || /^(__codelineno|__line)/i.test(name)) return "generated line anchor";
  if (/^<a\b[^>]*>\s*<\/a>$/i.test(trimmed)) return "empty anchor";
  return "content";
}

function main() {
  const arm0 = JSON.parse(fs.readFileSync(path.join(H.HERE, "results-arm0.json"), "utf8"));
  const AA = new Set(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]);
  const buckets = {};
  const pages = {};
  let aaTotal = 0, aaNoise = 0;
  const examples = [];

  for (const p of arm0.pages) {
    for (const v of p.violations || []) {
      const html = v.html || "";
      const kind = classify(html);
      const isAA = (v.tags || []).some((t) => AA.has(t));
      buckets[kind] = (buckets[kind] || 0) + 1;
      if (isAA) { aaTotal += 1; if (kind !== "content") aaNoise += 1; }
      pages[p.id] = (pages[p.id] || 0) + 1;
      if (kind !== "content" && examples.length < 25) examples.push({ page: p.id, rule: v.id, kind, html: html.slice(0, 140) });
    }
  }

  const total = Object.values(buckets).reduce((a, b) => a + b, 0);
  const out = {
    question: "how much of what axe reports is aimed at elements a page's author never intended a user to read?",
    method: "classification of axe's own reported node markup: an anchor with no content, or a syntax highlighter's line anchor",
    instances: total,
    by_kind: buckets,
    share_machine_generated: buckets["generated line anchor"] / total,
    share_empty_anchor: buckets["empty anchor"] / total,
    aa_instances: aaTotal,
    aa_non_content: aaNoise,
    aa_share_non_content: aaTotal ? aaNoise / aaTotal : null,
    worst_pages: Object.entries(pages).sort((a, b) => b[1] - a[1]).slice(0, 5),
    examples,
  };
  fs.writeFileSync(path.join(H.HERE, "results-oracle-noise.json"), JSON.stringify(out, null, 1) + "\n");
  console.log(`\n${total} arm-0 instances`);
  for (const [k, v] of Object.entries(buckets)) console.log(`  ${k.padEnd(18)} ${String(v).padStart(4)}  ${(v / total * 100).toFixed(1)}%`);
  console.log(`\nWCAG-tagged instances: ${aaTotal}, of which aimed at such elements: ${aaNoise} (${out.aa_share_non_content === null ? "n/a" : (out.aa_share_non_content * 100).toFixed(1) + "%"})`);
  console.log(`\nmost-reported pages: ${out.worst_pages.map(([id, n]) => `${id}=${n}`).join("  ")}`);
  for (const e of examples.slice(0, 5)) console.log(`  [${e.kind}] ${e.rule} ${e.page}: ${e.html}`);
}

main();