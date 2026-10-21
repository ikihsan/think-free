#!/usr/bin/env node
// E202 arms + oracle. One process, deterministic: page -> arm -> axe in jsdom.
// Page scripts are not executed (E162's rule, unchanged); every arm pays the
// same parse+serialize cost before axe sees it.
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const AXE_SRC = fs.readFileSync(require.resolve("axe-core"), "utf8");
const { JSDOM } = require("jsdom");
const PER_PAGE_TIMEOUT_MS = 240000;

// The strings the document itself carries. Anything an arm adds to this set is
// an invention, and E162's fabrication proxy is reused unchanged.
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

function withAxe(html, url) {
  const dom = new JSDOM(html, { url, runScripts: "outside-only", pretendToBeVisual: true });
  dom.window.eval(AXE_SRC);
  return dom;
}

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
        id: v.id, impact: v.impact, tags: v.tags, help: v.help,
        target: n.target, html: (n.html || "").slice(0, 400),
        wcag: (v.tags || []).filter((t) => /^wcag2(a|aa)$/.test(t)),
      });
    }
  }
  const incomplete = {};
  for (const v of r.incomplete || []) incomplete[v.id] = v.nodes.length;
  return { violations: slim, incomplete, testEngine: r.testEngine };
}

// --- the arms -------------------------------------------------------------

function parse(html, url) {
  const dom = new JSDOM(html, { url });
  return dom;
}

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
  return name !== null && !id;   // <a name="…"> with no href
}

const CSS_RULE = 'a[id^="__codelineno"],a[name^="__codelineno"],a[href=""]{visibility:hidden}';

function applyArm(html, arm) {
  const dom = parse(html, "https://e200.invalid/");
  const doc = dom.window.document;
  const before = visibleText(doc);
  const record = { rewritten: [], removed: [], css: false };

  if (arm === 1 || arm === 3) {
    const targets = [...doc.querySelectorAll("a, area")].filter(isSelfLink);
    for (const el of targets) {
      const keep = el.id || el.getAttribute("name") || el.getAttribute("href")?.slice(1) || "";
      if (arm === 3) { record.removed.push(keep); el.remove(); continue; }
      const span = doc.createElement("span");
      if (keep) span.id = keep;
      el.replaceWith(span);
      record.rewritten.push(keep);
    }
  } else if (arm === 2) {
    const style = doc.createElement("style");
    style.textContent = CSS_RULE;
    (doc.head || doc.documentElement).prepend(style);
    record.css = true;
  }

  const after = visibleText(doc);
  const added = [...after].filter((s) => !before.has(s));
  const out = dom.serialize();
  dom.window.close();
  return { html: out, record, addedStrings: added };
}

// K3: after the rewrite, does every fragment still resolve?
function targetSurvival(html, ids) {
  const dom = parse(html, "https://e200.invalid/");
  const doc = dom.window.document;
  const alive = ids.filter((id) => id && (doc.getElementById(id) ||
    doc.querySelector(`[name="${CSS.escape ? CSS.escape(id) : id}"]`)));
  dom.window.close();
  return { wanted: ids.length, alive: alive.length };
}

async function main() {
  const args = process.argv.slice(2);
  const mode = args[0] || "arms";            // "arms" | "control" | "sweep"
  const man = JSON.parse(fs.readFileSync(path.join(HERE, "corpus-manifest.json"), "utf8"));

  if (mode === "control") {
    const fx = fs.readFileSync(path.join(HERE, "fixtures/k1.html"), "utf8");
    const out = { fixture: "fixtures/k1.html", arms: {} };
    for (const arm of [0, 2]) {
      const r = applyArm(fx, arm);
      const dom = withAxe(r.html, "https://e200.invalid/k1");
      out.arms[arm] = await axeRun(dom);
      dom.window.close();
    }
    fs.writeFileSync(path.join(HERE, "results-control.json"), JSON.stringify(out, null, 2) + "\n");
    console.log(`control: arm0 link-name=${out.arms[0].violations.filter(v=>v.id==="link-name").length} ` +
                `arm2 link-name=${out.arms[2].violations.filter(v=>v.id==="link-name").length}`);
    return;
  }

  if (mode === "sweep") {
    // arm 0 over every HTTP-200 page: G0's "axe completes on >=90% of fetched
    // pages", computed once and shared by every later arm comparison.
    const pages = man.pages.filter((p) => p.status === 200);
    const out = { arm: 0, engine: null, pages: [] };
    let done = 0;
    for (const p of pages) {
      const html = fs.readFileSync(path.join(HERE, p.file), "utf8");
      const r = applyArm(html, 0);
      try {
        const dom = withAxe(r.html, p.url);
        const res = await axeRun(dom);
        dom.window.close();
        out.pages.push({ url: p.url, file: p.file, qualifies: !!p.qualifies,
          n: res.violations.length, wcag: res.violations.filter(v => v.wcag.length).length,
          rules: [...new Set(res.violations.map(v => v.id))], engine: res.testEngine,
          violations: res.violations });
        out.engine = res.testEngine;
      } catch (e) {
        out.pages.push({ url: p.url, file: p.file, qualifies: !!p.qualifies, error: String(e.message || e) });
      }
      done++;
      if (done % 10 === 0) console.log(`sweep ${done}/${pages.length}`);
    }
    fs.writeFileSync(path.join(HERE, "results-sweep-arm0.json"), JSON.stringify(out) + "\n");
    console.log(`sweep done: ${out.pages.filter(p=>!p.error).length}/${pages.length} axe runs ok`);
    return;
  }

  // arms on the qualifying population
  const pages = man.pages.filter((p) => p.qualifies);
  const out = { engine: null, pages: [] };
  for (const p of pages) {
    const html = fs.readFileSync(path.join(HERE, p.file), "utf8");
    const entry = { url: p.url, file: p.file, host: p.host, arms: {} };
    const base = applyArm(html, 0);
    for (const arm of [0, 1, 2, 3]) {
      const r = arm === 0 ? base : applyArm(html, arm);
      try {
        const dom = withAxe(r.html, p.url);
        const res = await axeRun(dom);
        dom.window.close();
        entry.arms[arm] = {
          violations: res.violations, incomplete: res.incomplete,
          addedStrings: r.addedStrings, record: r.record,
          engine: res.testEngine,
        };
        out.engine = res.testEngine;
        if (arm === 1 && r.record.rewritten.length) {
          entry.arms[1].survival = targetSurvival(r.html, r.record.rewritten);
        }
        if (arm === 3 && r.record.removed.length) {
          entry.arms[3].lostTargets = r.record.removed.length;
        }
      } catch (e) {
        entry.arms[arm] = { error: String(e.message || e) };
      }
    }
    out.pages.push(entry);
    console.log(`arms on ${p.host}: rewritten=${(entry.arms[1] && entry.arms[1].record || {}).rewritten?.length ?? "err"}`);
  }
  fs.writeFileSync(path.join(HERE, "results-arms.json"), JSON.stringify(out, null, 2) + "\n");
  console.log(`wrote results-arms.json for ${out.pages.length} qualifying pages`);
}

// Exported so sweep.js reuses this exact oracle instead of copying it; the
// recorded commands above still run main() identically.
if (require.main === module) {
  main().catch((e) => { console.error(e); process.exit(1); });
}
module.exports = { applyArm, axeRun, withAxe, visibleText, isSelfLink, targetSurvival };
