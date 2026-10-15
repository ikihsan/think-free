#!/usr/bin/env node
// Shared machinery: load a page, run axe-core in jsdom, count what matters.
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { JSDOM } = require("jsdom");

const HERE = path.join(__dirname, "..");
const AXE_SRC = fs.readFileSync(require.resolve("axe-core"), "utf8");

// Every user-facing string that a document already contains. A repair that
// draws a name from this set is quoting the page; a repair that draws from
// anywhere else invented it.
function visibleText(doc) {
  const out = new Set();
  const walk = (n) => {
    if (n.nodeType === 3) {
      const t = n.nodeValue.replace(/\s+/g, " ").trim();
      if (t) out.add(t.toLowerCase());
      return;
    }
    if (n.nodeType !== 1) return;
    for (const a of ["alt", "title", "aria-label", "placeholder", "value",
                     "name", "summary", "aria-describedby", "data-title"]) {
      const v = n.getAttribute && n.getAttribute(a);
      if (v && v.trim()) out.add(v.replace(/\s+/g, " ").trim().toLowerCase());
    }
    for (const c of n.children || []) walk(c);
  };
  walk(doc.body);
  return out;
}

function attrStrings(doc) {
  const out = new Set();
  const walk = (n) => {
    if (n.nodeType !== 1) return;
    for (const a of n.attributes || []) {
      if (/^(alt|title|aria-label|placeholder|value|name|summary)$/i.test(a.name)) {
        const v = a.value.replace(/\s+/g, " ").trim().toLowerCase();
        if (v) out.add(v);
      }
    }
    for (const c of n.children || []) walk(c);
  };
  walk(doc.documentElement);
  return out;
}

// Page scripts are NOT executed. `outside-only` gives us axe without running
// the corpus pages' own JavaScript: the experiment measures the DOM, and page
// scripts are both a source of non-determinism and third-party code we have
// no reason to execute. axe itself is injected through window.eval.
function withAxe(html, url) {
  const dom = new JSDOM(html, { url, runScripts: "outside-only", pretendToBeVisual: true });
  dom.window.eval(AXE_SRC);
  return dom;
}

const PER_PAGE_TIMEOUT_MS = 240000;

async function axeRun(dom) {
  const win = dom.window;
  const work = win.axe.run(win.document, { resultTypes: ["violations", "incomplete"] });
  let timer;
  const r = await Promise.race([
    work,
    new Promise((_, rej) => { timer = setTimeout(() => rej(new Error("axe timeout")), PER_PAGE_TIMEOUT_MS); }),
  ]).finally(() => clearTimeout(timer));
  const slim = [];
  for (const v of r.violations) {
    for (const n of v.nodes) {
      slim.push({
        id: v.id,
        impact: v.impact,
        tags: v.tags,
        help: v.help,
        target: n.target,
        failureSummary: n.failureSummary,
        html: (n.html || "").slice(0, 400),
      });
    }
  }
  const incomplete = {};
  for (const v of r.incomplete || []) incomplete[v.id] = v.nodes.length;
  return { violations: slim, incomplete, testEngine: r.testEngine, url: win.location.href };
}

// Round-trip through the serializer and re-parse: every arm pays this cost.
function roundTrip(html, url) {
  const first = new JSDOM(html, { url });
  const serialized = first.serialize();
  first.window.close();
  return serialized;
}

function loadCorpus() {
  const man = JSON.parse(fs.readFileSync(path.join(HERE, "corpus-manifest.json"), "utf8"));
  return man.pages.filter((p) => p.status === 200);
}

function htmlFor(page) {
  return fs.readFileSync(path.join(HERE, page.file), "utf8");
}

function readTextFile(rel) {
  return fs.readFileSync(path.join(HERE, rel), "utf8");
}

module.exports = {
  HERE, withAxe, axeRun, roundTrip, loadCorpus, htmlFor,
  visibleText, attrStrings, crypto,
};