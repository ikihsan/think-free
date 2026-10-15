#!/usr/bin/env node
// Why arm B eliminated nothing: the strongest objection to this experiment's
// result is "your repair table is too weak, a cleverer one could derive names
// the page does contain". This script answers that from the documents
// themselves, without any repair table at all.
//
// For every axe violation instance in the arm-0 record it takes the node
// markup axe itself reported (`html`, up to 400 bytes) and asks a question no
// repair policy is involved in: does this node carry ANY author-written string
// a repairer could read - its own text content, or an authored attribute on it?
//
// If the answer is "no" for the dominant rule class, the missing information is
// not in the document, and the conclusion is a property of these pages rather
// than a weakness of the program. That is the difference between a falsified
// mechanism and a broken instrument.
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");
const H = require("./lib/harness");

// Attributes that carry author-written, user-facing text. SVG geometry
// (`d`, `points`, `viewBox`) is deliberately excluded: it is not language and
// cannot be read aloud as a name.
//
// `name` is deliberately excluded too, and that exclusion is the result of a
// first version of this file: with `name` counted as a name, 94.8% of the 96
// `link-name` violations looked like they carried authored text, because 90 of
// them are Pygments code-line anchors - `<a id="__codelineno-0-1"
// name="__codelineno-0-1" href="#__codelineno-0-1"></a>` - whose `name` is a
// JavaScript anchor name. HTML `name` does not compute an accessible name on
// `<a>`; the accname specification uses it on `form`, `meta`, `iframe`, `map`,
// `param` and `slot` only.
const AUTHORED = ["alt", "title", "aria-label", "placeholder", "value", "summary", "aria-roledescription"];

// Rules whose defect IS a missing name: for these, "is there a string to read"
// is the question. The rest are structural defects, where the presence of text
// says nothing about whether a repair is derivable.
const NAME_DEFECT = new Set(["link-name", "label", "role-img-alt", "image-alt", "aria-dialog-name",
  "aria-progressbar-name", "frame-title", "aria-valid-attr-value", "aria-allowed-attr"]);

function measure(html) {
  let el = null;
  try {
    const dom = new JSDOM(`<!doctype html><body>${html}</body>`);
    el = dom.window.document.body.firstElementChild;
  } catch (e) { el = null; }
  const attrs = [];
  const strings = [];
  if (el) {
    for (const a of AUTHORED) {
      const v = el.getAttribute(a);
      if (v && v.trim()) { attrs.push(`${a}="${v.trim()}"`); strings.push(v.trim()); }
    }
    const t = (el.textContent || "").replace(/\s+/g, " ").trim();
    if (t) strings.push(t);
  } else {
    // Unparseable fragment (axe's html is truncated at 400 bytes, so the tail
    // can be a partial tag). Fall back to the bytes.
    const re = new RegExp(`\\b(${AUTHORED.join("|")})\\s*=\\s*"([^"]*)"`, "gi");
    let m;
    while ((m = re.exec(html))) if (m[2].trim()) { attrs.push(`${m[1]}="${m[2].trim()}"`); strings.push(m[2].trim()); }
    const t = html.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
    if (t) strings.push(t);
  }
  return { attrs, strings, has: strings.length > 0 };
}

function main() {
  const arm0 = JSON.parse(fs.readFileSync(path.join(H.HERE, "results-arm0.json"), "utf8"));
  const AA = new Set(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]);

  const byRule = {};
  const examples = [];
  let missing = 0, present = 0, nohtml = 0;

  for (const page of arm0.pages) {
    for (const v of page.violations || []) {
      const html = v.html || "";
      if (!html) { nohtml += 1; continue; }
      const m = measure(html);
      const r = byRule[v.id] || (byRule[v.id] = { instances: 0, with_authored: 0, aa: (v.tags || []).some((t) => AA.has(t)), samples: [] });
      r.instances += 1;
      if (m.has) { r.with_authored += 1; present += 1; }
      else {
        missing += 1;
        if (r.samples.length < 3) r.samples.push(html.slice(0, 150));
        if (examples.length < 60 && ["link-name", "label", "aria-dialog-name", "aria-progressbar-name", "frame-title", "role-img-alt", "image-alt"].includes(v.id)) {
          examples.push({ page: page.id, rule: v.id, html: html.slice(0, 180) });
        }
      }
    }
  }

  const rows = Object.entries(byRule)
    .map(([rule, r]) => ({ rule, name_defect: NAME_DEFECT.has(rule), instances: r.instances, with_authored: r.with_authored,
      share_with_authored: r.instances ? r.with_authored / r.instances : 0, samples: r.samples }))
    .sort((a, b) => b.instances - a.instances);

  const total = present + missing;
  // The number that bears on the mechanism: of the instances whose defect is a
  // missing name, how many had a name available anywhere in the reported node?
  const ndRows = rows.filter((r) => r.name_defect);
  const ndTotal = ndRows.reduce((a, r) => a + r.instances, 0);
  const ndPresent = ndRows.reduce((a, r) => a + r.with_authored, 0);
  const out = {
    question: "does the node axe reported carry any author-written string a repairer could read?",
    source: "results-arm0.json `html` per violation instance (axe's own node markup, truncated at 400 bytes)",
    instances_measured: total,
    with_authored: present,
    without_authored: missing,
    no_html_recorded: nohtml,
    overall_share_with_authored: total ? present / total : null,
    name_defect_instances: ndTotal,
    name_defect_with_authored: ndPresent,
    name_defect_share_with_authored: ndTotal ? ndPresent / ndTotal : null,
    by_rule: rows,
    examples,
  };
  fs.writeFileSync(path.join(H.HERE, "results-why-not.json"), JSON.stringify(out, null, 1) + "\n");

  console.log(`\nmeasured ${total} arm-0 instances (${nohtml} had no node markup recorded)`);
  console.log(`carry an author-written string: ${present} (${(out.overall_share_with_authored * 100).toFixed(1)}%)`);
  console.log(`carry none:                    ${missing} (${(100 - out.overall_share_with_authored * 100).toFixed(1)}%)\n`);
  console.log(`of the ${ndTotal} instances whose defect is a MISSING NAME, ${ndPresent} (${(out.name_defect_share_with_authored * 100).toFixed(1)}%) had any name available to read\n`);
  console.log("rule                          inst  with-authored  share  name-defect");
  for (const r of rows) {
    console.log(`  ${r.rule.padEnd(28)} ${String(r.instances).padStart(4)}  ${String(r.with_authored).padStart(13)}  ${(r.share_with_authored * 100).toFixed(1).padStart(5)}%  ${r.name_defect ? "yes" : "-"}`);
  }
  console.log("\nnodes with nothing a repairer could read (first of each rule):");
  for (const r of rows) {
    if (!r.samples.length) continue;
    console.log(`  ${r.rule}: ${r.samples[0]}`);
  }
}

main();