#!/usr/bin/env node
// E163's measurement: with the plumbing removed, what is left, and how much of
// it has a name written somewhere else in the same document?
//
// Two steps per instance, both declared in PROTOCOL.md before any page was
// fetched:
//
//   1. classify the instance with E162 section 4's rule, unchanged - a syntax
//      highlighter's line anchor or an empty anchor is plumbing, everything
//      else is content. Changing this after seeing the new pages' numbers would
//      be choosing the denominator to suit the answer.
//   2. for every CONTENT instance whose defect is a missing or wrong name,
//      probe the document for authored text in the declared order D1-D9 and
//      record which source answered, with the text it answered with.
//
// Every derivation is written to the output file, so a reader can check the
// judgement instead of taking it.
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");
const HERE = __dirname;
const E162 = path.join(HERE, "..", "162-a11y-deterministic-repair");

const AA = new Set(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]);
const isAA = (tags) => (tags || []).some((t) => AA.has(t));

// E162's rule, verbatim (EXPERIMENTS/162-*/oracle-noise.js).
function classify(html) {
  const trimmed = (html || "").trim();
  const id = (/<[^>]+\sid="([^"]*)"/.exec(trimmed) || [])[1] || "";
  const name = (/<[^>]+\sname="([^"]*)"/.exec(trimmed) || [])[1] || "";
  if (/^(__codelineno|__line|line-\d|hljs)/i.test(id) || /^(__codelineno|__line)/i.test(name)) return "generated line anchor";
  if (/^<a\b[^>]*>\s*<\/a>$/i.test(trimmed)) return "empty anchor";
  return "content";
}

// Rules whose defect IS a name, from E162's why-not.js. Unchanged.
const NAME_DEFECT = new Set(["link-name", "label", "role-img-alt", "image-alt", "aria-dialog-name",
  "aria-progressbar-name", "frame-title", "aria-valid-attr-value", "aria-allowed-attr",
  "button-name", "select-name", "aria-input-field-name", "aria-toggle-field-name",
  "aria-required-children", "aria-required-parent", "aria-roles", "aria-command-name",
  "aria-tooltip-name", "aria-treeitem-name", "aria-text", "aria-label", "form-field-multiple-labels",
  "accesskeys", "duplicate-id", "duplicate-id-active", "duplicate-id-aria", "duplicate-id-aria-owners"]);

// ---- locating the reported node inside the live document -------------------
// The arm-0 record stores axe's own node markup (truncated at 400 bytes), not
// its target selector, so the element is recovered by signature and the match's
// confidence is recorded. A signature match on a unique id, name, href/src or
// class is `confident`; a first-of-many match is `ambiguous` and is counted
// separately so the report can say how much rests on it.
function signature(html) {
  const h = (html || "").trim();
  const tag = (/^<([a-zA-Z0-9-]+)/.exec(h) || [])[1] || "";
  const attr = (n) => {
    const m = new RegExp(`\\s${n}="([^"]*)"`, "i").exec(h);
    return m ? m[1] : "";
  };
  return { tag, id: attr("id"), name: attr("name"), href: attr("href"), src: attr("src"),
    cls: attr("class"), type: attr("type"), role: attr("role") };
}

function locate(doc, html) {
  const s = signature(html);
  if (!s.tag) return { el: null, confidence: "none" };
  let cands = Array.from(doc.querySelectorAll(s.tag));
  if (!cands.length) return { el: null, confidence: "none" };
  const by = (fn) => cands.filter(fn);
  const pick = (list, how) => (list.length === 1 ? { el: list[0], confidence: how } : null);
  for (const [fn, how] of [
    [(e) => s.id && e.getAttribute("id") === s.id, "id"],
    [(e) => s.name && e.getAttribute("name") === s.name, "name"],
    [(e) => s.href && e.getAttribute("href") === s.href, "href"],
    [(e) => s.src && e.getAttribute("src") === s.src, "src"],
    [(e) => s.cls && e.getAttribute("class") === s.cls, "class"],
  ]) {
    const hit = pick(by(fn), how);
    if (hit) return hit;
  }
  return { el: cands[0], confidence: "first-of-many" };
}

// ---- the derivation probes, D1-D9 in the declared order --------------------
const txt = (el) => (el && el.textContent ? el.textContent.replace(/\s+/g, " ").trim() : "");

function byId(doc, id) {
  if (!id) return null;
  try { return doc.getElementById(id); } catch (e) { return null; }
}

function probe(doc, el) {
  if (!el) return null;
  const found = [];
  const push = (source, value, el2) => {
    const t = String(value || "").replace(/\s+/g, " ").trim();
    if (t) found.push({ source, text: t.slice(0, 160), node: el2 ? (el2.tagName || "").toLowerCase() : null });
  };

  // D1 / D2 - an explicit in-document reference.
  for (const [source, attrName] of [["D1", "aria-labelledby"], ["D2", "aria-describedby"]]) {
    const ref = el.getAttribute(attrName);
    if (!ref) continue;
    for (const id of ref.split(/\s+/)) {
      const t = txt(byId(doc, id));
      if (t) push(source, t, byId(doc, id));
    }
  }

  const tag = (el.tagName || "").toLowerCase();
  const type = (el.getAttribute("type") || "").toLowerCase();
  const isFormControl = tag === "input" || tag === "select" || tag === "textarea";
  const needsLabel = tag === "input" || tag === "select" || tag === "textarea";

  // D3 - an associated or wrapping <label>.
  if (needsLabel && !el.getAttribute("aria-label") && !el.getAttribute("aria-labelledby")) {
    const id = el.getAttribute("id");
    if (id) {
      for (const l of doc.querySelectorAll("label[for]")) {
        if (l.getAttribute("for") === id) { push("D3", txt(l), l); break; }
      }
    }
    const wrap = el.closest && el.closest("label");
    if (wrap && txt(wrap)) push("D3", txt(wrap), wrap);
  }

  // D4 - a figure caption for an image.
  if (tag === "img") {
    const fig = el.closest && el.closest("figure");
    const cap = fig && fig.querySelector("figcaption");
    if (cap) push("D4", txt(cap), cap);
  }

  // D5 - a title attribute on the element or its nearest labelled ancestor.
  {
    let node = el, hops = 0;
    while (node && hops < 3) {
      const t = node.getAttribute && node.getAttribute("title");
      if (t && t.trim()) { push("D5", t, node); break; }
      node = node.parentElement; hops += 1;
    }
  }

  // D6 - a submit control's own value.
  if (tag === "input" && (type === "submit" || type === "button" || type === "reset")) {
    push("D6", el.getAttribute("value"), el);
  }

  // D7 - a table header for a cell that has none.
  if (tag === "td" || tag === "th") {
    const table = el.closest && el.closest("table");
    if (table) {
      const row = el.parentElement;
      const idx = row ? Array.prototype.indexOf.call(row.children, el) : -1;
      const head = table.querySelector("thead tr") || table.querySelector("tr");
      const cell = head && idx >= 0 ? head.children[idx] : null;
      if (cell) push("D7", txt(cell), cell);
    }
  }

  // D8 - the nearest preceding heading. Declared as the aggressive probe: it is
  // how a documentation page's line anchors would acquire the code line beside
  // them, which E162 called cosmetic. Counted both ways in the analysis.
  {
    const heads = doc.querySelectorAll("h1,h2,h3,h4,h5,h6");
    let best = null;
    for (const h of heads) {
      if (h.compareDocumentPosition && (h.compareDocumentPosition(el) & 4)) best = h; // Node.DOCUMENT_POSITION_FOLLOWING = 4
    }
    if (best) push("D8", txt(best), best);
  }

  // D9 - the element's own text. Recorded so a D9 hit can be told apart from a
  // derivation: if it has its own text, axe had a name already.
  const own = txt(el);
  if (own) push("D9", own, el);

  if (isFormControl && !found.length) return { derivations: [], own_text: own || null };
  return { derivations: found, own_text: own || null, is_submit: type === "submit" };
}

function main() {
  const arm0 = JSON.parse(fs.readFileSync(path.join(HERE, "results-arm0.json"), "utf8"));
  const man162 = JSON.parse(fs.readFileSync(path.join(E162, "corpus-manifest.json"), "utf8"));
  const man163 = JSON.parse(fs.readFileSync(path.join(HERE, "corpus-manifest.json"), "utf8"));
  const fileFor = (page) => {
    if (page.arm === "1") {
      const m = man162.pages.find((x) => `162:${x.id}` === page.id);
      return m && fs.existsSync(path.join(E162, m.file)) ? path.join(E162, m.file) : null;
    }
    const m = man163.pages.find((x) => x.id === page.id);
    return m ? path.join(HERE, m.file) : null;
  };

  const rows = [];
  const confidence = {};
  let pages_loaded = 0;

  for (const page of arm0.pages) {
    const file = fileFor(page);
    if (!file) continue;
    let doc;
    try { doc = new JSDOM(fs.readFileSync(file, "utf8"), { url: page.url }).window.document; }
    catch (e) { continue; }
    pages_loaded += 1;
    for (const v of page.violations || []) {
      const kind = classify(v.html);
      const rec = {
        page: page.id, arm: page.arm, frame: page.frame, rule: v.id,
        aa: isAA(v.tags), impact: v.impact, kind,
        node: (v.html || "").slice(0, 180),
      };
      if (kind === "content") {
        const { el, confidence: how } = locate(doc, v.html);
        confidence[how] = (confidence[how] || 0) + 1;
        rec.match = how;
        if (el) {
          rec.tag = (el.tagName || "").toLowerCase();
          const p = probe(doc, el);
          rec.derivations = p.derivations;
          rec.own_text = p.own_text;
          rec.derivable = p.derivations.filter((d) => d.source !== "D9").map((d) => d.source);
          rec.derivable_d1_d7 = p.derivations.filter((d) => d.source !== "D9" && d.source !== "D8").map((d) => d.source);
        }
      }
      rows.push(rec);
    }
  }

  const out = {
    question: "with E162's plumbing removed, what is left, and how much of it has a name written elsewhere in the same document?",
    method: "E162 section 4's plumbing rule unchanged; node recovered from axe's recorded markup by signature (confidence recorded); D1-D9 probed in the declared order",
    pages_measured: pages_loaded,
    instances: rows.length,
    match_confidence: confidence,
    rows,
  };
  fs.writeFileSync(path.join(HERE, "results-derivation.json"), JSON.stringify(out, null, 1) + "\n");
  const byKind = {};
  for (const r of rows) byKind[r.kind] = (byKind[r.kind] || 0) + 1;
  console.log(`\n${rows.length} instances over ${pages_loaded} pages`);
  for (const [k, v] of Object.entries(byKind)) console.log(`  ${k.padEnd(22)} ${String(v).padStart(4)}`);
  console.log(`\nnode match confidence: ${JSON.stringify(confidence)}`);
}

main();